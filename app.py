import os
import itertools
from functools import wraps
from flask import Flask, flash, render_template, session, redirect, request, url_for
from flask_pymongo import PyMongo
from passlib.hash import pbkdf2_sha256
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)


app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["MONGO_DBNAME"] = 'mad_libz'
app.secret_key = os.environ.get('SECRET')

mongo = PyMongo(app)


# Function decorator is used for other functions to check if website visitor is logged in
def check_logged_in(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        if 'logged-in' in session:
            return(func(*args, **kwargs))
        else:
            return render_template('no-login.html')
    return wrapped_function

# Renders the home.html page
@app.route('/')
@check_logged_in
def home():
    return render_template('home.html', username=session['user-name'])

# Provides paths for accessing the register page and for attempting to register
@app.route('/register', methods=["GET", "POST"])
def register():
    if 'user-id' in session:
        return redirect(url_for('home'))
    else:
        if request.method == "GET":
            return render_template('register.html')
        elif request.method == "POST":
            username = request.form['userid']
            user = mongo.db.user_info.find_one({
                'username': username})
            if user is None:
                password = request.form['password']
                _hash = pbkdf2_sha256.hash(password)
                mongo.db.user_info.insert_one({
                    'username': username,
                    'password': _hash
                })
                flash('New user successfully created')
                return redirect(url_for('login'))
            else:
                return render_template('register.html',
                                       error="User already exists")

# Provides paths for accessing login page and for logging into website
@app.route('/login', methods=["GET", "POST"])
def login():
    if 'user-id' in session:
        return redirect(url_for('home'))
    else:
        if request.method == "GET":
            return render_template('login.html')
        elif request.method == "POST":
            username = request.form['userid']
            user = mongo.db.user_info.find_one({'username': username})
            user_password = user['password']
            form_password = request.form['password']
            if pbkdf2_sha256.verify(form_password, user_password):
                session['logged-in'] = True
                session['user-name'] = username
                session['user-id'] = str(user['_id'])
            else:
                return render_template('login.html',
                                       error="Incorrect credentials")
            flash('You were successfully logged in')
            return redirect(url_for('home'))

# Logs user out
@app.route('/logout')
@check_logged_in
def logout():
    session.pop('logged-in', None)
    session.pop('user-name', None)
    session.pop('user-id', None)
    return redirect(url_for('home'))

# Renders create.html page where users first choose mad lib template to use
@app.route('/create')
@check_logged_in
def create():
    return render_template('create.html',
                           skeletons=mongo.db.mad_libz_templates.find())

# Page accessed after choosing theme, where user can give word inputs
@app.route('/insert_words', methods=['GET'])
@check_logged_in
def insert_words():
    selected_id = request.args.get('mad_lib')
    mad_lib = mongo.db.mad_libz_templates.find_one(
                                                  {'_id': ObjectId(selected_id)
                                                   })
    return render_template('insert-words.html', mad_lib=mad_lib)

# Adds user input data into the MongoDB database
@app.route('/push_data/<template_id>', methods=['POST'])
@check_logged_in
def push_data(template_id):
    user_input = list(request.form.values())
    inserted_id = mongo.db.mad_libz_input.insert_one({
        "mad_lib_id": ObjectId(template_id),
        "words": user_input,
        "creatorID": session['user-id']
    }).inserted_id
    return redirect(url_for('display_result', inserted_id=inserted_id,
                            skeleton_id=template_id))

# Renders result of chosen theme with user inputs zipped into templates
@app.route('/display_result/<inserted_id>/<skeleton_id>')
@check_logged_in
def display_result(inserted_id, skeleton_id):
    user_input = mongo.db.mad_libz_input.find_one(
                                            {'_id': ObjectId(inserted_id)})
    if session['user-id'] == user_input['creatorID']:
        skeleton = mongo.db.mad_libz_templates.find_one(
                                            {'_id': ObjectId(skeleton_id)})
        script = skeleton['script']
        user_input_words = user_input['words']
        result = tuple(itertools.zip_longest(script, user_input_words))
        result = [tuple('' if i is None else i for i in t) for t in result]
        result = " ".join(map(" ".join, result))
        creator = mongo.db.user_info.find_one(
                                            {'_id': ObjectId
                                             (user_input['creatorID'])})
        username = creator['username']
        return render_template('results.html', user_input=user_input,
                               skeleton=skeleton, result=result,
                               username=username)
    else:
        return render_template('home.html',
                               invalid_user="Sorry, invalid user")

# Renders library.html page, displaying all Mad Libs stored in the database
@app.route('/display_all')
@check_logged_in
def display_all():
    user_inputs = list(mongo.db.mad_libz_input.find())
    for user_input in user_inputs:
        skeleton = mongo.db.mad_libz_templates.find_one(
                                        {'_id': ObjectId(
                                            user_input['mad_lib_id'])})
        script = skeleton['script']
        user_input_words = user_input['words']
        result = tuple(itertools.zip_longest(script, user_input_words))
        result = [tuple('' if i is None else i for i in t) for t in result]
        result = " ".join(map(" ".join, result))
        user_input['mad_lib'] = result
        user_input['title'] = skeleton['title']
        creator = mongo.db.user_info.find_one(
                                            {'_id': ObjectId
                                             (user_input['creatorID'])})
        user_input['username'] = creator['username']
    return render_template('library.html', user_inputs=user_inputs,
                           user_input=user_input)

# Renders page where users can change prefilled input fields (prefilled with latest data)
@app.route('/edit/<mad_lib_id>')
@check_logged_in
def edit(mad_lib_id):
    user_input = mongo.db.mad_libz_input.find_one(
                                                 {'_id': ObjectId(mad_lib_id)})
    if session['user-id'] == user_input['creatorID']:
        skeleton = mongo.db.mad_libz_templates.find_one(
                                                    {'_id': ObjectId(
                                                     user_input['mad_lib_id'])
                                                     })
        descriptors = skeleton['descriptors']
        words = user_input['words']
        user_prefill = zip(descriptors, words)
        return render_template('edit.html', mad_lib_id=mad_lib_id,
                               user_prefill=user_prefill)
    else:
        return render_template('home.html',
                               invalid_user="Sorry, invalid user")

# Updates data/user input provided on the Mad Lib and redirects to library.html
@app.route('/update/<mad_lib_id>', methods=['POST'])
@check_logged_in
def update(mad_lib_id):
    user_input = list(request.form.values())
    user = mongo.db.mad_libz_input.find_one(
                                            {'_id': ObjectId(mad_lib_id)})
    if session['user-id'] == user['creatorID']:
        mongo.db.mad_libz_input.update_one(
                                        {'_id': ObjectId(mad_lib_id)},
                                        {'$set': {"words": user_input}}
        )
        flash('Mad Lib was updated')
        return redirect(url_for('display_all'))
    else:
        return render_template('home.html',
                               invalid_user="Sorry, invalid user")

# Delete route that removes record from database
@app.route('/delete/<mad_lib_id>')
@check_logged_in
def delete(mad_lib_id):
    user = mongo.db.mad_libz_input.find_one({'_id': ObjectId(mad_lib_id)})
    if session['user-id'] == user['creatorID']:
        mongo.db.mad_libz_input.remove({'_id': ObjectId(mad_lib_id)})
        flash('Mad Lib was deleted')
        return redirect(url_for('display_all'))
    else:
        return render_template('home.html',
                               invalid_user="Sorry, invalid user")


# Defines IP address and PORT of application
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
