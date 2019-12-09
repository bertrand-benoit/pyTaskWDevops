#!/bin/env python3

import re
import os
import configparser
from azure.devops.connection import Connection
from azure.devops.v5_1.work_item_tracking.models import Wiql
from msrest.authentication import BasicAuthentication
from taskw import TaskWarrior

WIQL_QUERY_FILE: str = 'azure_devops_wiql.query'

config = configparser.ConfigParser()
config.read(os.path.expanduser(os.path.join('~', '.config/task_warrior_azure_devops.conf')))

personal_access_token: str = config['AzureDevops']['personal_access_token']
organization_url: str = config['AzureDevops']['organization_url']
project: str = config['AzureDevops']['project']
current_sprint: str = config['AzureDevops']['current_sprint']
assignee: str = config['AzureDevops']['assignee']
max_wiql_results: int = int(config['AzureDevops']['max_wiql_results'])
max_description_length: int = int(config['General']['max_desc_length'])
keyword_tag_replace_map: dict = dict(config.items('KeywordAndTagReplace'))

AZURE_ITEM_FINAL_STATES: list = ['Closed', 'Removed']


def get_azure_devops_work_items(team_project, iteration_path, assigned_to):
    with open(os.path.join(os.path.dirname(__file__), WIQL_QUERY_FILE), 'r') as f:
        query_raw = f.read()
    query_params = {'team_project': team_project, 'assigned_to': assigned_to, 'iteration_path': iteration_path}

    credentials = BasicAuthentication('', personal_access_token)
    connection = Connection(base_url=organization_url, creds=credentials)
    wit_client = connection.clients.get_work_item_tracking_client()
    wiql = Wiql(query=query_raw.format(**query_params))
    wiql_results = wit_client.query_by_wiql(wiql, top=max_wiql_results).work_items
    if not wiql_results:
        return []

    # WIQL query gives a WorkItemReference with ID only
    # => we get the corresponding WorkItem from id
    work_items_raw = (wit_client.get_work_item(int(res.id)) for res in wiql_results)
    return [{'id': work_item_raw.id,
             'type': work_item_raw.fields["System.WorkItemType"],
             'state': work_item_raw.fields["System.State"],
             'title': work_item_raw.fields["System.Title"]} for work_item_raw in work_items_raw]


def get_taskwarrior_tasks(taskwarrior_project):
    tasks = task_warrior.load_tasks()
    return [t for t in tasks['pending'] if t['project'].lower() == taskwarrior_project]


def find_taskwarrior_from_azure_devops_id(work_item_id, task_list):
    return [t for t in task_list if t['description'].startswith(str(work_item_id))]


def format_description(desc, tag_list):
    for keyword, tag in keyword_tag_replace_map.items():
        desc, count = re.subn(r'[/\s[]*\b' + keyword + r'\b[]/\s]*', '', desc, flags=re.IGNORECASE)
        if count and tag:
            tag_list.append(tag)

    return desc if len(desc) <= max_description_length else f"{desc[:max_description_length]}..."


# Task Warrior tasks load.
task_warrior = TaskWarrior()

print(f'Loading "{project}" Task warriors pending tasks ...')
tw_tasks = get_taskwarrior_tasks(project.lower())
print(f'Found {len(tw_tasks)} tasks.')

# Azure Devops current sprint's tasks load.
print(f'Loading "{project}" Azure Devops work items ...')
work_items = get_azure_devops_work_items(project, current_sprint, assignee)
print(f'Found {len(work_items)} work items.')

for work_item in work_items:
    # Checks if there is already a time warrior task for this Azure Devops item.
    existing_tw = find_taskwarrior_from_azure_devops_id(work_item['id'], tw_tasks)

    if existing_tw:
        # There is already a Task Warrior task for this Azure Devops Work items.
        # Checks its state.
        if work_item['state'] in AZURE_ITEM_FINAL_STATES:
            print(f'{work_item["id"]}: updating state to "done" for completed task {existing_tw[0]}')
            task_warrior.task_done(uuid=existing_tw[0]['uuid'])
        else:
            print(f'{work_item["id"]}: nothing more to do, found an existing task with good state in task warrior.')
    elif work_item['state'] not in AZURE_ITEM_FINAL_STATES:
        tags = []
        description = f'{work_item["id"]} - ' + format_description(work_item['title'], tags)
        print(f'{work_item["id"]}: Creating a new task with description "{description}", and tags "{tags}".')
        task_warrior.task_add(description, project=project.lower(), tags=tags)
