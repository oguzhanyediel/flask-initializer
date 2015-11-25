# flask-initializer
A simple python script to initialize a new flask project aka boiler plate
* basic folder structure
* project_name.wsgi
* \__init__.py
* dbconnect.py (MySQL connection)
* virtualenv initialization
  * Flask
  * flask-login
  * flask-bcrypt
  * WTForms
  * MySQL-python
  * requests
  * passlib

### Basic usage
To initialize a new project in your current working directory simply use the following line:

> sudo python create_project.py -n Project_Name

### You can also specify a path where the project is supposed to be created:
> sudo python create_project.py -n Project_Name -p /path/to/project

### Raspberry Pi usecase
If you are trying to setup a development flask server on the Raspberry Pi you are going to get an error by the time the script tries to install flask-bcrypt
To fix this try doing the following:

> sudo apt-get install libffi-dev

