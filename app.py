import os
from os import path

if path.exists("env.py"):
    import env

from flask import Flask, render_template, redirect, request, url_for, flash, session
import bcrypt
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'cooking'
app.config['MONGO_URI'] = os.environ.get('MONGO_URI','mongodb://localhost')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)



''' start of code from Anthony Herbert -> Pretty Printed '''
@app.route('/')
def index():
    return render_template('index.html',  title="Community Cookbook")


@app.route('/logout')
def logout():
    session.clear()
    flash('You are logged out', 'info')
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'username' : request.form['username']})
        
        if not login_user:
            flash('Incorrect username', "warning")
    
        if login_user:
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['username'] = request.form['username']
                flash('You are logged in', 'success')
                return render_template("index.html", username=session['username'],
                        recipes=mongo.db.recipes.find(),courses=mongo.db.meal_courses.find())
            flash('Incorrect password', 'danger')  

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'username' : request.form['username'], 'password' : hashpass, 'email' : request.form['email']})
            flash('You have successfully created your account - now you can login', 'success')
            return render_template('login.html')
        
        flash('That username already exists!-please choose a different one', 'warning')

    if 'username' in session:
        flash( 'You are logged in as ' + session['username'], 'success')
        return render_template('register.html')

    return render_template('register.html')

''' end of code from Anthony Herbert -> Pretty Printed '''

@app.route('/enter_recipe')
def enter_recipe():
    if 'username' in session:
        recipes=mongo.db.recipes.find()
        cuisines=mongo.db.cuisines.find().sort('cuisine_name',1)
        meal_course=mongo.db.meal_course.find().sort('course_name',1)
        main_ingredient=mongo.db.main_ingredient.find().sort('main_ingredient',1)
        return render_template('enter_recipe.html', recipes=recipes, 
                                cuisines=cuisines, main_ingredient=main_ingredient, 
                                meal_course=meal_course, cook_name=session['username'])
    else:
        flash('You must be logged in to add a recipe', 'warning')
        return render_template('login.html')


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    req = request.form

    recipes.insert_one({
        'recipe_name':req.get('recipe_name'),
        'cook_name': session['username'],
        'cuisine_name':req.get('cuisine_name'),
        'main_ingredient':req.get('main_ingredient'),
        'prep_time': req.get('prep_time'),
        'total_cooking_time': req.get('total_cooking_time'),
        'servings': req.get('servings'),
        'ingredients':req.get('ingredients').splitlines(),
        'instructions':req.get('instructions').splitlines(),
        'image_src':req.get('image_src'),
        'meal_course':req.get('meal_course'),
        'protein':req.get('protein'),
        'fat_per_serve':req.get('fat_per_serve'),
        'carbohydrate':req.get('carbohydrate'),
        'dietary_fibre':req.get('dietary_fibre'),
        'cholesterol':req.get('cholesterol'),
        'energy':req.get('energy'),
        })
    flash('Your recipe has been successfully added!', 'success')
    return redirect(url_for('show_recipes'))


@app.route('/show_one_recipe/<recipe_id>')
def show_one_recipe(recipe_id):
    the_recipe=mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("show_one_recipe.html", recipes=the_recipe)

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    cuisines=mongo.db.cuisines.find().sort('cuisine_name',1)
    meal_course=mongo.db.meal_course.find().sort('course_name',1)
    main_ingredient=mongo.db.main_ingredient.find().sort('main_ingredient',1)
    return render_template("edit_recipe.html", cuisines=cuisines, meal_course=meal_course, main_ingredient=main_ingredient,
    recipe=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}))


@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update_one({'_id': ObjectId(recipe_id)},
    {
        '$set':{
    'recipe_name': request.form.get('recipe_name'),
    'cook_name': request.form.get('cook_name'),
    'cuisine_name':request.form.get('cuisine_name'),
    'main_ingredient':request.form.get('main_ingredient'),
    'prep_time': request.form.get('prep_time'),
    'total_cooking_time': request.form.get('total_cooking_time'),
    'servings': request.form.get('servings'),
    'ingredients':request.form.get('ingredients').splitlines(),
    'instructions':request.form.get('instructions').splitlines(),
    'image_src':request.form.get('image_src'),
    'meal_course':request.form.get('meal_course'),
    'protein':request.form.get('protein'),
    'fat_per_serve':request.form.get('fat_per_serve'),
    'carbohydrate':request.form.get('carbohydrate'),
    'dietary_fibre':request.form.get('dietary_fibre'),
    'cholesterol':request.form.get('cholesterol'),
    'energy':request.form.get('energy')
    }})
    flash('Recipe updated.')
    return redirect(url_for('show_recipes'))

@app.route('/show_recipes')
def show_recipes():
    recipes=mongo.db.recipes.find().collation({'locale':'en'}).sort('recipe_name', 1)
    return render_template("show_recipes.html", recipes=recipes)

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    flash('Recipe deleted.', 'success')
    return redirect(url_for('show_recipes'))

@app.route('/browse')
def browse():
    recipes=mongo.db.recipes.find().sort('recipe_name', 1)
    return render_template("browse.html", recipes=recipes)


''' The below routes handle administration of cuisine types '''

@app.route('/cuisines')
def cuisines():
    if 'username' in session:
        return render_template("cuisines.html",title='Cuisines', cuisines=mongo.db.cuisines.find().collation({'locale':'en'}).sort('cuisine_name',1))
    else:
        flash('You must be logged in to add or edit a cuisine', 'warning')
        return render_template('login.html')

@app.route('/edit_cuisine/<cuisines_id>')
def edit_cuisine(cuisines_id):
    
    return render_template('edit_cuisine.html',
    cuisines=mongo.db.cuisines.find_one({'_id': ObjectId(cuisines_id)}))

@app.route('/update_cuisine/<cuisines_id>', methods=['POST'])
def update_cuisine(cuisines_id):
    mongo.db.cuisines.update(
        {'_id': ObjectId(cuisines_id)},
        {'cuisine_name': request.form.get('cuisine_name')})
    return redirect(url_for('cuisines'))

@app.route('/delete_cuisine/<cuisines_id>', methods = ['POST', 'GET'])
def delete_cuisine(cuisines_id):
    the_cuisine = mongo.db.cuisines.find_one({"_id": ObjectId(cuisines_id)})['created_by']
    current_user =  session['username']
    created_by = the_cuisine

    if created_by != current_user:
        flash("hi fucker")
        return redirect(url_for('cuisines'))

    else:
        flash("ffs")    
    
    return redirect(url_for('cuisines'))

@app.route('/insert_cuisine', methods=['POST'])
def insert_cuisine():
    if request.method == 'POST':
        cuisines=mongo.db.cuisines
        existing_cuisine = cuisines.find_one({'cuisine_name' : request.form['cuisine_name']})
        if existing_cuisine:
            flash('This cuisine is already available', 'warning')
        if existing_cuisine is None:
            cuisine_doc = {'cuisine_name': request.form.get('cuisine_name'),
                    'created_by' : session['username']}
            cuisines.insert_one(cuisine_doc)
            flash('Your cuisine has been added', 'success')
    return redirect(url_for('cuisines'))

@app.route('/add_cuisine')
def add_cuisine():
    if request.method =='POST':
        flash ('Cuisine updated!')
    return render_template('add_cuisine.html', title='Add cuisine')










if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), 
    port=os.environ.get("PORT"), debug=True)