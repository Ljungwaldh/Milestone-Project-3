import os
from functools import wraps
from flask import Flask, render_template, session, redirect, request, url_for
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


def check_logged_in(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        if 'logged-in' in session:
            return(func(*args, **kwargs))
        else:
            return render_template('no-login.html')
    return wrapped_function


@app.route('/')
@check_logged_in
def home():
    return render_template('home.html', username=session['user-name'])


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    elif request.method == "POST":
        username = request.form['userid']
        user = mongo.db.user_info.find_one({
            'username': username})
        if user == None:
            password = request.form['password']
            _hash = pbkdf2_sha256.hash(password)
            mongo.db.user_info.insert_one({
                'username': username,
                'password': _hash
            })
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error="User already exists")


@app.route('/login', methods=["GET", "POST"])
def login():
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
            return "login error"
        return redirect(url_for('home'))


@app.route('/logout')
@check_logged_in
def logout():
    session.pop('logged-in', None)
    session.pop('user-name', None)
    session.pop('user-id', None)
    return redirect(url_for('home'))


@app.route('/create')
@check_logged_in
def create():
    return render_template('create.html',
                           skeletons=mongo.db.mad_libz_templates.find())


@app.route('/insert_words', methods=['GET'])
@check_logged_in
def insert_words():
    selected_id = request.args.get('mad_lib')
    mad_lib = mongo.db.mad_libz_templates.find_one(
                                                  {'_id': ObjectId(selected_id)
                                                   })
    return render_template('insert-words.html', mad_lib=mad_lib)


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
        result = tuple(zip(script, user_input_words))
        result = " ".join(map(" ".join, result))
        return render_template('results.html', user_input=user_input,
                               skeleton=skeleton, result=result)
    else:
        return render_template('invalid-user.html')


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
        result = tuple(zip(script, user_input_words))
        result = " ".join(map(" ".join, result))
        user_input['mad_lib'] = result
        user_input['title'] = skeleton['title']
    return render_template('library.html', user_inputs=user_inputs)


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
        return render_template('invalid-user.html')


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
        return redirect(url_for('display_all'))
    else:
        return render_template('invalid-user.html')


@app.route('/delete/<mad_lib_id>')
@check_logged_in
def delete(mad_lib_id):
    user = mongo.db.mad_libz_input.find_one({'_id': ObjectId(mad_lib_id)})
    if session['user-id'] == user['creatorID']:
        mongo.db.mad_libz_input.remove({'_id': ObjectId(mad_lib_id)})
        return redirect(url_for('display_all'))
    else:
        return render_template('invalid-user.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
