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


@app.route('/')
def hello():
    return 'Hello World'


@app.route('/create')
def create():
    return render_template('create.html',
                           skeletons=mongo.db.mad_libz_templates.find())


@app.route('/insert_words', methods=['GET'])
def insert_words():
    selected_id = request.args.get('mad_lib')
    mad_lib = mongo.db.mad_libz_templates.find_one(
                                                  {'_id': ObjectId(selected_id)
                                                   })
    return render_template('insert-words.html', mad_lib=mad_lib)


@app.route('/push_data/<template_id>', methods=['POST'])
def push_data(template_id):
    user_input = list(request.form.values())
    inserted_id = mongo.db.mad_libz_input.insert_one({
        "mad_lib_id": ObjectId(template_id),
        "words": user_input
    }).inserted_id
    return redirect(url_for('display_result', inserted_id=inserted_id,
                            skeleton_id=template_id))


@app.route('/display_result/<inserted_id>/<skeleton_id>')
def display_result(inserted_id, skeleton_id):
    user_input = mongo.db.mad_libz_input.find_one(
                                            {'_id': ObjectId(inserted_id)})
    skeleton = mongo.db.mad_libz_templates.find_one(
                                          {'_id': ObjectId(skeleton_id)})
    script = skeleton['script']
    user_input_words = user_input['words']
    result = tuple(zip(script, user_input_words))
    result = " ".join(map(" ".join, result))
    return render_template('results.html', user_input=user_input,
                           skeleton=skeleton, result=result)


@app.route('/display_all/<mad_libz_id>/<template_id>')
def display_all():



if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
