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


### Raspberry Pi usecase
If you are trying to setup a development flask server on the Raspberry Pi you are likely going to get an error by the time the script tries to install flask-bcrypt.

To fix this try doing the following:

> sudo apt-get install libffi-dev

