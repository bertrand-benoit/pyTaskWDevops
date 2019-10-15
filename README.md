# Task warrior and Azure Devops synchronizer version 1.0.0
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/abf1cfe570bb46f9b03c815fbd375fd2)](https://www.codacy.com/manual/bertrand-benoit/pyTaskWDevops?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=bertrand-benoit/pyTaskWDevops&amp;utm_campaign=Badge_Grade)

This is a free tool allowing to synchronize [Azure Devops](https://azure.microsoft.com/en-us/solutions/devops/) Work items with local [Task warrior](https://taskwarrior.org/).

Features:

-   creates new Task warrior item for each missing Azure Devops Work item
-   marks 'done' Task warrior item when corresponding Azure Devops Work item is completed
-   various regex patterns can be configured to format Task name according to your criteria

## Installation
You can either create a Virtual Environment (recommended if you use several Python projects) or not.

### Create a Virtual Environment
In the project main directory, you can execute the following instruction to create a *venv* environment:
```bash
python3 -m venv venv
```

Then you can activate it (will be effective only in the Terminal where you execute the instruction):
```bash
source venv/bin/activate
```

At any time, you can move back to your default environment:
```bash
deactivate
```

### Install dependencies
The project provides a **requirements.txt** file defining dependencies.

To install them, execute (add the `--user` option at end of command line, if you do NOT use Virtual environment):
```bash
pip3 install -r requirements.txt
```

## Configuration files
You must create your own configuration file **~/.config/task_warrior_azure_devops.conf**, adapting this tool to your account and your environment.

You can create your configuration file from the [sample](misc/task_warrior_azure_devops.conf.sample) provided in this project, under **misc/task_warrior_azure_devops.conf.sample**.

## Usage
### Prerequisites
Before using this tool, you must:

-   install [Task warrior](https://taskwarrior.org/)
-   create a [Personal Access Token](https://docs.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate)
-   create your configuration file from the provided [sample](misc/task_warrior_azure_devops.conf.sample)

### Samples
For easiest access, you can add the main directory of the project to your **$PATH**.

You can launch directly the tool:
```bash
task_warrior_azure_devops.py
```

## Contributing
Don't hesitate to [contribute](https://opensource.guide/how-to-contribute/) or to contact me if you want to improve the project.
You can [report issues or request features](https://github.com/bertrand-benoit/pyTaskWDevops/issues) and propose [pull requests](https://github.com/bertrand-benoit/pyTaskWDevops/pulls).

## Versioning
The versioning scheme we use is [SemVer](http://semver.org/).

## Authors
[Bertrand BENOIT](mailto:contact@bertrand-benoit.net)

## License
This project is under the GPLv3 License - see the [LICENSE](LICENSE) file for details
