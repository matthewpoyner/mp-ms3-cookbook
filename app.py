import os
from os import path

if path.exists("env.py"):
    import env

from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'cooking'
app.config['MONGO_URI'] = os.environ.get('MONGO_URI','mongodb://localhost')

mongo = PyMongo(app)

@app.route('/')
def index():
    a_recipe = mongo.db.recipes.find()
    return render_template("recipes.html", recipes=mongo.db.recipes.find())



@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html", recipes=mongo.db.recipes.find())

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), 
    port=os.environ.get("PORT"), debug=True)