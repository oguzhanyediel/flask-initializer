#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocessing import Process
import subprocess
import itertools
import argparse
import time
import sys
import os

DEBUG = False 

def create_structure(path, dir_exists):
	try:
		### Check if the given path exists, if not try to mkdir it ###
		if not dir_exists:
			os.mkdir(os.path.join(base_path, args.name))
		### Create folder structure ###
		os.mkdir(os.path.join(path, args.name, args.name))
		os.mkdir(os.path.join(path, args.name, args.name, "static"))
		os.mkdir(os.path.join(path, args.name, args.name, "static", "css"))
		os.mkdir(os.path.join(path, args.name, args.name, "static", "js"))
		os.mkdir(os.path.join(path, args.name, args.name, "static", "fonts"))
		os.mkdir(os.path.join(path, args.name, args.name, "templates"))
		### Create "/base_path/project/project.wsgi" ###
		with open(os.path.join(path, args.name, "{0}.wsgi".format(args.name.lower())), "w") as wsgi_file:
			wsgi_file.write(wsgi)
		### Create "/base_path/project/project/__init__.py" ###
		with open(os.path.join(path, args.name, args.name, "__init__.py"), "w") as init_file:
			init_file.write(init)
		### Create "/base_path/project/project/dbconnect.py" ###
		with open(os.path.join(path, args.name, args.name, "dbconnect.py"), "w") as db_file:
			db_file.write(dbconnect)
		print("\nDone creating folder structure, initializing virtualenv.\n")
		create_venv(os.path.join(path, args.name, args.name))
	except Exception as e:
		if DEBUG:
			print(str(e))
		print("An error occured, the folder structure probably already exist. Please check.")
		sys.exit(0)

def spinning_circle():
	### Function to show a spinning circle to indicate that the program is working in the background ###
	spinner = itertools.cycle(['-', '/', '|', '\\'])
	while True:
		sys.stdout.write(next(spinner))  # write the next character
		time.sleep(.1)
		sys.stdout.flush()                # flush stdout buffer (actual character display)
		sys.stdout.write('\b') 

def create_venv(path):
	if os.path.exists(path):
		### Start showing spinning circle to indicate that the program is working in the background ###
		cond = True
		thread = Process(target=spinning_circle)
		thread.daemon
		thread.start()
		### Start installing packages and python modules ###
		proc = subprocess.Popen("sudo apt-get install -y libffi-dev python-dev mysql-client \
								 mysql-server virtualenv", shell=True,
								 stdout=open("/dev/null", "w"), stderr=open("/dev/null", "w"))
		proc.wait()
		proc1 = subprocess.Popen("sudo virtualenv {0}/venv".format(path), shell=True, 
								 stdout=open("/dev/null", "w"), stderr=open("/dev/null", "w"))
		proc1.wait()
		proc2 = subprocess.Popen("sudo {0}/venv/bin/pip install --upgrade pip".format(path),
								 shell=True, stdout=open("/dev/null", "w"), stderr=open("/dev/null", "w"))
		proc2.wait()
		proc3 = subprocess.Popen("sudo {0}/venv/bin/pip install requests[security] Flask \
								 passlib mysql-python".format(path), shell=True, stdout=open("/dev/null", "w"), 
								 stderr=open("/dev/null", "w"))
		proc3.wait()
		proc4 = subprocess.Popen("sudo {0}/venv/bin/python {1}/venv/bin/pip install WTForms flask-login \
								 flask-bcrypt Flask-Mail".format(path, path), shell=True,
								 stdout=open("/dev/null", "w"), stderr=open("/dev/null", "w"))
		proc4.wait()
		thread.terminate()
	else:
		print("create_venv not valid")


if __name__ == "__main__":
	### Create a parser to parse the arguments given in the commandline ###
	parser = argparse.ArgumentParser()
	parser.add_argument("-n", "--name", dest="name", type=str, help="Your project name")
	parser.add_argument("-p", "--path", dest="path", type=str, 
						help="Path to where your project will go")
	args = parser.parse_args()

	### Print type and content or arguments when debugging ###
	if DEBUG:
		try:
			print(type(args.name), " - ", args.name)
			print(type(args.path), " - ", args.path)
		except Exception as e:
			print("Exception: " + str(e))

	### If a path is specified and that path exists, use it as base_path, else use this files path ###
	if (args.path != None) and (os.path.exists(args.path)):
		base_path = args.path 
	elif (args.path != None) and not (os.path.exists(args.path)):
		try:
			os.mkdir(args.path)
			base_path = args.path
		except:
			print("No valid path specified, using this files location as base path.")
			base_path = os.path.dirname(os.path.abspath(__file__))
	else:    
		base_path = os.path.dirname(os.path.abspath(__file__))
		print("No path specified, using this files location as base path.")

	### Default content of "project.wsgi" ###
	wsgi = """# -*- coding: utf-8 -*-
import sys
import os

venv_dir = "{0}"

activate_this = os.path.join(venv_dir, "bin", "activate_this.py")
execfile(activate_this, dict(__file__=activate_this))
sys.path.insert(0, "{1}")
sys.path.append(venv_dir)

from {2} import app as application
application.secret_key = "secretkeyherewhateverthatmaybe" 
""".format(os.path.join(base_path, args.name, args.name, "venv"), 
		   os.path.join(base_path, args.name),
		   args.name)

	### Default content of "__init__.py" ###
	init = """# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, redirect, flash, request, session
from dbconnect import connection
import logging
import os

log_dir = "/tmp/"

if not os.path.isdir(log_dir):
	os.mkdir(log_dir)

### Setting up the logger ###
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(os.path.join(log_dir, {0}))
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

### Initilizing the app ###
app = Flask(__name__)

@app.route("/")
def index():
	return "This is working..."

""".format(args.name)

	### Default content of "dbconnect.py" ###
	dbconnect = """#-*- coding: utf-8 -*-
import MySQLdb

### mysql --user=root -p ###
def connection():
	conn = MySQLdb.connect(host="localhost",
						   user="root",
						   passwd="",
						   db="")
	c = conn.cursor()
	return c, conn"""

	### Prompt the user to continue or not if a folder with the project name already exists ###
	if (os.path.isdir(os.path.join(base_path, args.name))):
		ans = raw_input("That folder already exists. Continue anyway? (Y/N)\n> ")
		if (ans.lower() == "y") or (ans.lower() == ("yes")):
			create_structure(base_path, True)
		else:
			print("Exiting...")
			sys.exit(0)
	else:
		create_structure(base_path, False)

	### If the program gets to this point everything went well ###
	print("\nSuccessfully created the flask project {0} at {1}{2}".format(args.name, args.path, args.name))
