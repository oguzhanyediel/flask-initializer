# -*- coding: utf-8 -*-
import argparse
import os
import sys
import subprocess

DEBUG = False

def create_venv(path):
    if os.path.exists(path):
        subprocess.call("sudo virtualenv {0}/venv".format(path), shell=True)
        subprocess.call("sudo {0}/venv/bin/python {1}/venv/bin/pip install Flask MySQL-python \
                        requests passlib".format(path, path), shell=True)
        subprocess.call("sudo {0}/venv/bin/python {1}/venv/bin/pip install WTForms flask-login \
                        flask-bcrypt".format(path, path), shell=True)
    else:
        print "create_venv not valid"

def create_structure(path, dir_exists):
    try:
        ### Create folder structure ###
        if not dir_exists:
            os.mkdir(os.path.join(base_path, args.name))
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
        ### Create "/base_path/project/project/run.py" ###
        with open(os.path.join(path, args.name, args.name, "run.py"), "w") as run_file:
            run_file.write(run)
        ### Create "/base_path/project/project/views.py" ###
        with open(os.path.join(path, args.name, args.name, "views.py"), "w") as views_file:
            views_file.write(views)
        ### Create "/base_path/project/project/dbconnect.py" ###
        with open(os.path.join(path, args.name, args.name, "dbconnect.py"), "w") as db_file:
            db_file.write(dbconnect)
        print "Done creating folder structure, initializing virtualenv."
        create_venv(os.path.join(path, args.name, args.name))
    except Exception as e:
        print "An error occured, the folder structure probably already exist. Please check."
        sys.exit(0)

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
            print type(args.name), " - ", args.name
            print type(args.path), " - ", args.path
        except Exception as e:
            print "Exception: " + str(e)

    ### If a path is specified and that path exists, use it as base_path, else use this files path ###
    if (args.path != None) and (os.path.exists(args.path)):
        base_path = args.path 
    elif (args.path != None) and not (os.path.exists(args.path)):
        try:
            os.mkdir(args.path)
            base_path = arg.path
        except:
            print "No valid path specified, using this files location as base path."
            base_path = os.path.dirname(os.path.abspath(__file__))
    else:    
        base_path = os.path.dirname(os.path.abspath(__file__))
        print "No path specified, using this files location as base path."

    ### Default content of "project.wsgi" ###
    wsgi = """# -*- coding: utf-8 -*-
import sys
import os

venv_dir = "{0}"

activate_this = os.path.join(venv_dir, "bin", "activate_this.py")
execfile(activate_this, dict(__file__=activate_this))
sys.path.insert(0, "{1}")
sys.path.append(venv_dir)

from FlaskApp import app as application
application.secret_key = "secretkeyherewhateverthatmaybe" 
""".format(os.path.join(base_path, args.name, args.name, "venv"), 
           os.path.join(base_path, args.name))

    ### Default content of "__init__.py" ###
    init = """# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, redirect, flash, request, session
from dbconnect import connection
import logging

log_dir = "{0}"

if not os.path.isdir(log_dir):
    os.mkdir(log_dir)

### Setting up the logger ###
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(os.path.join(log_dir, "logdir.log"))
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

### Initilizing the app ###
app = Flask(__name__)

import {1}.views""".format(os.path.join(base_path, args.name, "log"), args.name)
    
    ### Default content for run.py ###
    run = """# -*- coding: utf-8 -*-
from {0} import app

app.run(debug=True)""".format(args.name)

    ### Default content for views.py ###
    views = """# -*- coding: utf-8 -*-
from {0} import app, logger

### Adding route for the homepage "www.example.com/" ###
@app.route("/")
def homepage():
    return 'It worked, now to add content...' """.format(args.name)

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
            print "Exiting..."
            sys.exit(0)
    else:
        create_structure(base_path, False)
