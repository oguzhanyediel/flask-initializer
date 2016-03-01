# flask-initializer
A simple python script to initialize a new flask project aka boiler plate
* basic folder structure
* project.wsgi for wsgi deployment
* \__init__.py
* run.py
* views.py
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

> sudo python create_project.py -n ProjectName

#### You can also specify a path where the project is supposed to be created:

> sudo python create_project.py -n ProjectName -p /path/to/folder


#### For example:
Project name: flask-initializer
Path: /home/pascal/

> sudo python create_project.py -n flask-initializer -p /home/pascal/

Folder structure will look like this:

/home/pascal/flask-initializer

---- flask-initializer.wsgi

---- flask-initializer/

-------- __init__.py

-------- dbconnect.py

-------- run.py

-------- views.py

-------- templates/

-------- static/

------------ css/

------------ fonts/

------------ js/

-------- venv/

------------ virtualenv stuff ...

------------ ...

------------ ...
