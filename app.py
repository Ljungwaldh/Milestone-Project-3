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


@app.route('/display_all')
def display_all():
    user_inputs = list(mongo.db.mad_libz_input.find())
    for user_input in user_inputs:
        skeleton = mongo.db.mad_libz_templates.find_one(
                                        {'_id': ObjectId(user_input['mad_lib_id'])})
        script = skeleton['script']
        user_input_words = user_input['words']
        result = tuple(zip(script, user_input_words))
        result = " ".join(map(" ".join, result))
        user_input['mad_lib'] = result
        user_input['title'] = skeleton['title']
    return render_template('library.html', user_inputs=user_inputs)


@app.route('/edit/<mad_lib_id>')
def edit(mad_lib_id):
    user_input = mongo.db.mad_libz_input.find_one(
                                                 {'_id': ObjectId(mad_lib_id)})
    skeleton = mongo.db.mad_libz_templates.find_one(
                                                 {'_id': ObjectId(user_input['mad_lib_id'])})
    descriptors = skeleton['descriptors']
    words = user_input['words']
    user_prefill = zip(descriptors, words)
    return render_template('edit.html', mad_lib_id=mad_lib_id, user_prefill=user_prefill)


@app.route('/update/<mad_lib_id>', methods=['POST'])
def update(mad_lib_id):
    user_input = list(request.form.values())
    mongo.db.mad_libz_input.update_one(
                                      {'_id': ObjectId(mad_lib_id)},  
                                      {'$set': {"words": user_input}}
    )
    return redirect(url_for('display_all'))


@app.route('/delete/<mad_lib_id>')
def delete(mad_lib_id):
    mongo.db.mad_libz_input.remove({'_id': ObjectId(mad_lib_id)})
    return redirect(url_for('create'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
