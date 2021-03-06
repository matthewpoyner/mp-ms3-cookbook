import os
from os import path

if path.exists("env.py"):
    import env

from flask import (Flask, render_template, redirect,
                   request, url_for, flash, session)
import bcrypt
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'cooking'
app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://localhost')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',  title="World Community Cookbook")


@app.route('/logout')
def logout():
    # clear the session and flash a confirmation information message
    session.clear()
    flash('You have logged out successfully - see you soon', 'info')
    return render_template('index.html', title='Logged out')


''' The code here '''
''' is by Anthony Herbert -> Pretty Printed '''
''' https://www.youtube.com/watch?v=vVx1737auSE '''


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'username': request.form['username']})

        if not login_user:
            flash('Incorrect username', "warning")

        if login_user:
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['username'] = request.form['username']
                flash(session['username'] + ' you have logged in successfully!', 'success')
                return render_template("show_own_recipes.html", login_user=login_user,
                                       recipes=mongo.db.recipes.find(),
                                       courses=mongo.db.meal_courses.find(),
                                       title='Welcome '+session['username'])
            flash('Incorrect password', 'danger')

    return render_template('login.html', title='Login')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'username': request.form['username'],
                              'password': hashpass, 'email': request.form['email'], 'role': 'user'})
            flash('You have successfully created your account - now you can login', 'success')
            return render_template('login.html')
        flash('That username already exists!-please choose a different one', 'warning')

    if 'username' in session:
        flash('You are logged in as ' + session['username'], 'success')
        return render_template('register.html')

    return render_template('register.html', title='Sign Up!')

''' End of code '''
''' by Anthony Herbert -> Pretty Printed '''
''' https://www.youtube.com/watch?v=vVx1737auSE '''

''' Recipe section '''


@app.route('/enter_recipe')
def enter_recipe():
    if 'username' in session:
        recipes = mongo.db.recipes.find()
        cuisines = mongo.db.cuisines.find().collation({'locale': 'en'}).sort('cuisine_name', 1)
        meal_course = mongo.db.meal_course.find().collation({'locale': 'en'}).sort('course_name', 1)
        main_ingredient = mongo.db.main_ingredient.find().sort(
                                                        'main_ingredient', 1)
        return render_template('enter_recipe.html', title='Enter a new recipe',
                               recipes=recipes,
                               cuisines=cuisines,
                               main_ingredient=main_ingredient,
                               meal_course=meal_course,
                               cook_name=session['username'])
    else:
        flash('You must be logged in to add a recipe', 'warning')
        return render_template('login.html', title='Login to add recipe')


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    req = request.form
    recipes.insert_one({
        'recipe_name': req.get('recipe_name'),
        'cook_name': session['username'],
        'cuisine_name': req.get('cuisine_name'),
        'main_ingredient': req.get('main_ingredient'),
        'prep_time': req.get('prep_time'),
        'total_cooking_time': req.get('total_cooking_time'),
        'servings': req.get('servings'),
        'ingredients': req.get('ingredients').splitlines(),
        'instructions': req.get('instructions').splitlines(),
        'image_src': req.get('image_src'),
        'meal_course': req.get('meal_course'),
        'protein': req.get('protein'),
        'fat_per_serve': req.get('fat_per_serve'),
        'carbohydrate': req.get('carbohydrate'),
        'dietary_fibre': req.get('dietary_fibre'),
        'cholesterol': req.get('cholesterol'),
        'energy': req.get('energy'),
        })
    recipe = req.get('recipe_name')
    flash(f'Your recipe for {recipe} has been successfully added!', 'success')
    return redirect(url_for('show_recipes', recipes=recipes))


@app.route('/show_one_recipe/<recipe_id>')
def show_one_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    if 'username' not in session:
        current_user = ""
        return render_template("show_one_recipe.html", recipes=the_recipe, current_user=current_user)
    else:
        cook_name = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})['cook_name']
        current_user = session['username']
        user_role = mongo.db.users.find_one({"username": current_user})['role']
        return render_template("show_one_recipe.html",
                               recipes=the_recipe,
                               current_user=current_user,
                               user_role=user_role,
                               cook_name=cook_name)




@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    cuisines = mongo.db.cuisines.find().collation({'locale': 'en'}).sort('cuisine_name', 1)
    meal_course = mongo.db.meal_course.find().collation({'locale': 'en'}).sort('course_name', 1)
    main_ingredient = mongo.db.main_ingredient.find().collation({'locale': 'en'}).sort('main_ingredient', 1)
    recipes = mongo.db.recipes.find()
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    cook_name = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})['cook_name']
    if 'username' not in session:
        current_user = ""
        role = ""
        flash('You must be logged in to edit your own recipes', 'warning')
        return redirect(url_for('show_recipes', recipes=recipes, role=role))
    else:
        current_user = session['username']
        user_role = mongo.db.users.find_one({"username": current_user})['role']
        if user_role == 'admin':
            return render_template('edit_recipe.html',
                                   recipe=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}),
                                   cuisines=cuisines,
                                   meal_course=meal_course,
                                   main_ingredient=main_ingredient)
        if current_user == cook_name:
            return render_template('edit_recipe.html',
                                   recipe=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}),
                                   cuisines=cuisines,
                                   meal_course=meal_course,
                                   main_ingredient=main_ingredient)
        else:
            flash(
                'You can only edit recipes which you have created', 'warning'
                )
            return render_template('show_recipes.html', recipe=recipe)


@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    req = request.form
    recipes.update_one(
        {'_id': ObjectId(recipe_id)},
        {
         '$set': {
          'recipe_name': req.get('recipe_name'),
          'cook_name': session['username'],
          'cuisine_name': req.get('cuisine_name'),
          'main_ingredient': req.get('main_ingredient'),
          'prep_time': req.get('prep_time'),
          'total_cooking_time': req.get('total_cooking_time'),
          'servings': req.get('servings'),
          'ingredients': req.get('ingredients').splitlines(),
          'instructions': req.get('instructions').splitlines(),
          'image_src': req.get('image_src'),
          'meal_course': req.get('meal_course'),
          'protein': req.get('protein'),
          'fat_per_serve': req.get('fat_per_serve'),
          'carbohydrate': req.get('carbohydrate'),
          'dietary_fibre': req.get('dietary_fibre'),
          'cholesterol': req.get('cholesterol'),
          'energy': req.get('energy')
         }
          })
    recipe = req.get('recipe_name')
    flash(f'Recipe {recipe} updated.', 'success')
    return redirect(url_for('show_recipes'))


@app.route('/show_recipes')
def show_recipes():
    recipes = mongo.db.recipes.find().collation({'locale': 'en'}).sort('recipe_name', 1)
    return render_template("show_recipes.html", recipes=recipes,
                           title='Browse recipes')


@app.route('/show_own_recipes')
def show_own_recipes():
    recipes = mongo.db.recipes.find()
    current_user = session['username']
    return render_template('show_own_recipes.html', current_user=current_user, recipes=recipes)

@app.route('/search_recipes')
def search_recipes():
    return render_template('search_recipes.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    return render_template("search_results.html", recipes=recipes)


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    recipes = mongo.db.recipes.find()
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    cook_name = mongo.db.recipes.find_one(
                                         {"_id": ObjectId(recipe_id)}
                                         )['cook_name']
    current_user = session['username']
    user_role = mongo.db.users.find_one({"username": current_user})['role']
    if 'username' not in session:
        current_user = ""
        role = ""
        flash('You must be logged in to delete your own recipes', 'danger')
        return redirect(url_for('show_recipes', recipes=recipes, role=role))
    else:
        if user_role == 'admin':
            mongo.db.recipes.delete_one({'_id': ObjectId(recipe_id)})
            flash('Recipe deleted.', 'success')
            return redirect(url_for('show_recipes'))
        if current_user == cook_name:
            mongo.db.recipes.delete_one({'_id': ObjectId(recipe_id)})
            flash('Recipe deleted.', 'success')
            return redirect(url_for('show_recipes'))
        else:
            flash(
                'You can only delete recipes which you have created', 'danger'
                )
            return render_template('show_recipes.html')


''' The routes below handle administration of cuisine types '''


@app.route('/cuisine_admin')
def cuisine_admin():
    if 'username' in session:
        return render_template("cuisine_admin.html", title='Cuisines',
                               cuisines=mongo.db.cuisines.find().collation(
                                   {'locale': 'en'}).sort('cuisine_name', 1))
    else:
        flash('You must be logged in to add or edit a cuisine', 'warning')
        return render_template('login.html')


@app.route('/edit_cuisine/<cuisines_id>')
def edit_cuisine(cuisines_id):
    created_by = mongo.db.cuisines.find_one(
        {"_id": ObjectId(cuisines_id)})['created_by']
    current_user = session['username']
    user_role = mongo.db.users.find_one({"username": current_user})['role']
    created_by = created_by
    if user_role == 'admin':
        return render_template('edit_cuisine.html',
                               cuisines=mongo.db.cuisines.find_one(
                                   {'_id': ObjectId(cuisines_id)}))
    if created_by != current_user:
        flash('You can only edit cuisines which you have created', 'warning')
        return redirect(url_for('cuisine_admin'))
    else:
        return render_template('edit_cuisine.html',
                               cuisines=mongo.db.cuisines.find_one(
                                   {'_id': ObjectId(cuisines_id)}))


@app.route('/update_cuisine/<cuisines_id>', methods=['POST'])
def update_cuisine(cuisines_id):
    if request.method == 'POST':
        cuisines = mongo.db.cuisines.find()
        edited_cuisine = request.form['cuisine_name']
        cuisine = mongo.db.cuisines

        for existing in cuisines:
            if existing['cuisine_name'].lower() == edited_cuisine.lower():
                flash('This option is already available!', 'danger')
                return redirect(url_for('cuisines', cuisines=cuisines))
        else:
            cuisine.update_one({'_id': ObjectId(cuisines_id)},
                               {
                                '$set': {
                                 'cuisine_name': request.form.get(
                                     'cuisine_name'),
                                 'created_by': session['username']
                                }})
            flash('Your cuisine has been updated')

            return redirect(url_for('cuisines'))

        return redirect(url_for('cuisines'))


@app.route('/delete_cuisine/<cuisines_id>', methods=['POST', 'GET'])
def delete_cuisine(cuisines_id):
    cuisines = mongo.db.cuisines
    created_by = cuisines.find_one(
        {"_id": ObjectId(cuisines_id)})['created_by']
    current_user = session['username']
    user_role = mongo.db.users.find_one({"username": current_user})['role']
    created_by = created_by
    if user_role == 'admin':
        cuisines.delete_one({'_id': ObjectId(cuisines_id)})
        flash('Cuisine successfully deleted', 'success')
        return redirect(url_for('cuisine_admin'))
    if created_by != current_user:
        flash('You can only delete cuisines which you have created', 'warning')
        return redirect(url_for('cuisine_admin'))
    else:
        cuisines.delete_one({'_id': ObjectId(cuisines_id)})
        flash('Cuisine successfully deleted', 'success')
        return redirect(url_for('cuisine_admin'))
    return redirect(url_for('cuisine_admin'))


@app.route('/insert_cuisine', methods=['POST', 'GET'])
def insert_cuisine():
    if request.method == 'POST':
        cuisines = mongo.db.cuisines.find()
        new_cuisine = request.form['cuisine_name']
        cuisine = mongo.db.cuisines
        for existing in cuisines:
            if existing['cuisine_name'].lower() == new_cuisine.lower():
                flash('This option is already available!', 'danger')
                return redirect(url_for('cuisine_admin', cuisines=cuisines))
        else:
            cuisine_doc = ({'cuisine_name': request.form.get('cuisine_name'),
                            'created_by': session['username']})
            cuisine.insert_one(cuisine_doc)
            flash('Your cuisine has been added', 'success')
            return redirect(url_for('cuisine_admin', cuisines=cuisines))
    return redirect(url_for('cuisine_admin', cuisines=cuisines))


@app.route('/add_cuisine')
def add_cuisine():
    if 'username' not in session:
        return render_template('index.html', title="World Community Cookbook")
    else:
        return render_template('add_cuisine.html', title='Add New Cuisine')


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=os.environ.get("PORT"), debug=True)
