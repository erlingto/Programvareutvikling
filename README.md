# ![pageres](matega/static/imgs/matega.jpg)
[![pipeline status](https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-23/badges/master/pipeline.svg)](https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-23/commits/master)

## What is Matega?
Matega is an environmentally driven business, working towards reducing food waste by giving you high-quality recipes based off what you have in your fridge!

Link to repository: [Matega - Gruppe 23](https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-23).


## Frameworks and plugins
The Matega webapp is based on the [Django Web Framework](https://www.djangoproject.com/) (version >=2.1.5).

The following notable third party plugins are installed:
* [Django Allauth](https://django-allauth.readthedocs.io/en/latest/index.html)
* [Django Autocomplete Light](https://django-autocomplete-light.readthedocs.io/en/master/index.html)
* [Django PWA](https://pypi.org/project/django-pwa/)
* [Django REST Framework](https://www.django-rest-framework.org/)
* [Requests](http://www.python-requests.org/en/latest/)

## Features

* Register to get your own personal fridge!
* Add igredients to your fridge to keep track of what you have!
* Get a list of recipes made by our approved chefs - only the best meals are good enough!
* Are you a chef? Send in an application and you might get approved from our staff!

## Installation

### Setting up a virtual environment

1. If not already installed, [download python 3 from this website](https://www.python.org/downloads/)
2. Pip should be included in the python package, if not, [get pip from here](https://pip.pypa.io/en/stable/installing/)
3. Create a virtual environment by using the following command:
```
python3 -m venv mategaenv
```
Whereas "mategaenv" can be renamed to whatever you want.
**NOTE:** The python command might vary between systems. If `python3` doesn't work, try `py` instead if you're on a Windows machine.
this guide will use `python3` for commands, adapt where necessary.

4. 
* **Windows** users has to run the `activate.bat`-file within the `Scripts`-folder of their virtual environment via a terminal window to activate it.
* **Mac and GNU/Linux** users use the command `source path/to/bin/activate`, just replace `path/to` with the required folders. The bin-folder is directly inside the created
virtual environment.
5. Onwards!

### The website

**The next steps are implying that a virtual environment is activated**

1. Start by cloning the git repo (or fork it if that's your jam):
```
git clone https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-23.git
```
2. Enter the newly created `gruppe-23`-folder with a terminal window and run the following command:
```
pip3 install -r requirements.txt
```
If the `pip3` command doesn't work, use `pip` instead.

3. Create a database if nonexistant with the following command: 
```
python3 manage.py migrate
```
**NOTE: for safety reasons, the operational database located at `matega.recipes` is not included in the repo. Hence, you will only get a local test database.**

4. Start the local testing server with
```
python3 manage.py runserver
```

5. Good luck!


## How to use
For a user manual and other useful info, [check out our wiki](https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-23/wikis/home).

## License
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This repository is licensed under the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html). From the GNU license webpage:
> Developers who write software can release it under the terms of the GNU GPL. When they do, it will be free software and stay free software, 
no matter who changes or distributes the program. We call this copyleft: the software is copyrighted, but instead of using those rights to restrict 
users like proprietary software does, we use them to ensure that every user has freedom.

> Using the GNU GPL will require that all the released improved versions be free software. 
This means you can avoid the risk of having to compete with a proprietary modified version of your own work.

> The GPL does not require you to release your modified version, or any part of it. 
You are free to make modifications and use them privately, without ever releasing them. 
This applies to organizations (including companies), too; 
an organization can make a modified version and use it internally without ever releasing it outside the organization.

> But if you release the modified version to the public in some way, the GPL requires you to make the modified source code available to the program's users, under the GPL.

> Thus, the GPL gives permission to release the modified program in certain ways, and not in other ways; but the decision of whether to release it is up to you.

## Contributors
* Alexander Fredheim (Backend developer)
* [Andreas Langnes](https://github.com/Realfsen) (Fullstack developer)
* Erling Tømte (Backend developer)
* Helene Hogna (Frontend developer)
* Nina Aarvik (Frontend & backend developer)
* Silje Marie Moksnes (Frontend deveoper)
