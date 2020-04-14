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
app.secret_key = "secrets123"

mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template("index.html", recipes=mongo.db.recipes.find())

@app.route('/enter_recipe')
def enter_recipe():
    recipes=mongo.db.recipes.find()
    cuisine=mongo.db.cuisine.find().sort('cuisine_name',1)
    main_ingredient=mongo.db.main_ingredient.find().sort('main_ingredient',1)
    return render_template('enter_recipe.html', recipes=recipes, cuisine=cuisine, main_ingredient=main_ingredient)


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one({
        'recipe_name':request.form['recipe_name'],
        'cook_name':request.form['cook_name'],
        'cuisine_name':request.form['cuisine_name'],
        'main_ingredient':request.form['main_ingredient'],
        'prep_time':request.form['prep_time'],
        'total_cooking_time':request.form['total_cooking_time'],
        'fat_per_serve':request.form['fat_per_serve'],
        'ingredients':request.form['ingredients'],
        'instructions':request.form['instructions']
    })
    return render_template('index.html')


@app.route('/show_recipes')
def show_recipes():
    recipes=mongo.db.recipes.find().sort('recipe_name', 1)
    return render_template("show_recipes.html", recipes=recipes)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), 
    port=os.environ.get("PORT"), debug=True)