import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)


app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["MONGO_DBNAME"] = 'mad_libz'

mongo = PyMongo(app)


noun1 = "apple"
noun2 = "banana"
adjective1 = "big"
adjective2 = "small"
verb_ing = "running"


mad_lib_templates = {"templates": [
    {"title": "Test 1",
     "script": f"This is a test, here is a {noun1}. Now I am {verb_ing} towards a {adjective1} {noun2}",
     "theme": "test1"
     },
    {"title": "Test 2",
     "script": f"This is a test, here is a {noun2}. Now I am {verb_ing} towards a {adjective2} {noun1}",
     "theme": "test2"
     }
]}


@app.route('/')
def hello():
    return 'Hello World'


@app.route('/read', methods=['GET'])
def hello2():
    return mad_lib_templates


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)