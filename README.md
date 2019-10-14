# Task warrior and Azure Devops synchronizer version 1.0.0

This is a free tool allowing to synchronize Azure Devops Work items with local Task warrior.

Features:

 - creates new Task warrior item for each missing Azure Devops Work item
 - marks 'done' Task warrior item when corresponding Azure Devops Work item is completed
 - various regex patterns can be configured to format Task name according to your criteria

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

You can create your configuration file from the sample provided in this project, under **misc/task_warrior_azure_devops.conf.sample**.

## Contributing
Don't hesitate to [contribute](https://opensource.guide/how-to-contribute/) or to contact me if you want to improve the project.
You can [report issues or request features](https://github.com/bertrand-benoit/pyTaskWDevops/issues) and propose [pull requests](https://github.com/bertrand-benoit/pyTaskWDevops/pulls).

## Versioning
The versioning scheme we use is [SemVer](http://semver.org/).

## Authors
[Bertrand BENOIT](mailto:contact@bertrand-benoit.net)

## License
This project is under the GPLv3 License - see the [LICENSE](LICENSE) file for details
