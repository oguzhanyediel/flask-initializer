# flask-initializer
A simple python script to initialize a new flask project
* basic folder structure
* project_name.wsgi
* \__init__.py
* dbconnect.py (MySQL connection)

#### TODO:
* virtualenv initialization

### Basic usage
To initialize a new project in your current working directory simply use the following line:

> python create_project.py -n Project_Name

### You can also specify a path where the project is supposed to be created:

> python create_project.py -n Project_Name -p /path/to/project
