# -*- coding: utf-8 -*-
import argparse
import os
import sys

DEBUG = False

def create_structure(dir_exists):
    try:
        ### Create folder structure ###
        if not dir_exists:
            os.mkdir(os.path.join(base_path, args.name))
        os.mkdir(os.path.join(base_path, args.name, args.name))
        os.mkdir(os.path.join(base_path, args.name, args.name, "static"))
        os.mkdir(os.path.join(base_path, args.name, args.name, "static", "css"))
        os.mkdir(os.path.join(base_path, args.name, args.name, "static", "js"))
        os.mkdir(os.path.join(base_path, args.name, args.name, "static", "fonts"))
        os.mkdir(os.path.join(base_path, args.name, args.name, "templates"))
        ### Create "/base_path/project/project.wsgi" ###
        with open(os.path.join(base_path, args.name, "%s.wsgi" % args.name.lower()), "w") as wsgi_file:
            wsgi_file.write(wsgi)
        ### Create "/base_path/project/project/__init__.py" ###
        with open(os.path.join(base_path, args.name, args.name, "__init__.py"), "w") as init_file:
            init_file.write(init)
        ### Create "/base_path/project/project/dbconnect.py" ###
        with open(os.path.join(base_path, args.name, args.name, "dbconnect.py"), "w") as db_file:
            db_file.write(dbconnect)
        print "Done."
    except OSError:
        print "An error occured, the folder structure probably already exist. Please make sure."
        sys.exit(0)


if __name__ == "__main__":
    ### Create a parser to parse the arguments given in the commandline ###
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", dest="name", type=str, help="Your project name")
    parser.add_argument("-p", "--path", dest="path", type=str, help="Path to where your project will go")
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
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
        print "No valid path specified, using this files location as base path."

    ### Default content of "project.wsgi" ###
    wsgi = """# -*- coding: utf-8 -*-
import sys
import os

venv_dir = "%s"

activate_this = os.path.join(venv_dir, "bin", "activate_this.py")
execfile(activate_this, dict(__file__=activate_this))
sys.path.insert(0, "%s")
sys.path.append(venv_dir)

from FlaskApp import app as application
application.secret_key = "secretkeyherewhateverthatmaybe"
""" % (os.path.join(base_path, args.name, args.name, "venv"), os.path.join(base_path, args.name))

    ### Default content of "__init__.py" ###
    init = """# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, redirect, flash, request, session
from dbconnect import connection
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as guard
import logging
import gc

log_dir = "/var/www-data/"
if not os.path.isdir(log_dir):
    os.mkdir(log_dir)

### Setting up the logger ###
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(os.path.join(log_dir, "logfile.log"))
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

### Initilizing the app ###
app = Flask(__name__)

### Adding route for the homepage "www.example.com/" ###
@app.route("/")
def homepage():
    return 'It worked, now to add content...' """

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
            create_structure(True)
        else:
            print "Exiting..."
            sys.exit(0)
    else:
        create_structure(False)