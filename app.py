#  Copyright (c) 2020. Bryan S Mullen. All rights reserved.


################################################################
# Imports
################################################################


import os
import secrets
import random
import boto3

from flask import Flask, flash, render_template, redirect, request, session, \
    url_for
from flask_pymongo import PyMongo

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, SelectField, FileField, TextAreaField, \
    SubmitField
from wtforms.validators import DataRequired

from statistics import mean
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

if os.path.exists("env.py"):
    import env

################################################################
# App Initialization
################################################################


#  app init
app = Flask(__name__)

# mongo init
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
mongo = PyMongo(app)

# s3 init
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID'),
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
s3 = boto3.client(
    's3',
    AWS_ACCESS_KEY_ID=AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY=AWS_SECRET_ACCESS_KEY
)
s3_url = 'https://bryansmullen-whats-for-dinner.s3-eu-west-1.amazonaws.com/'

################################################################
# Home & Account Routes
################################################################


'''
GET - Returns the home.html template
'''


@app.route('/')
def home():
    return render_template('home.html')


'''
GET - Returns the user page in the account.html template. Masks the password.
'''


@app.route('/account/')
def account():
    try:
        uid = session['uid']
        user = mongo.db.users.find_one({'_id': ObjectId(uid)}, {'password': 0})
        if session['uid']:
            try:
                recipes_list = user['recipes']
                recipes = mongo.db.recipes.find({'_id': {'$in': recipes_list}})
            except:
                recipes = []
                print('Error finding recipes')
            return render_template('account.html', user=user, recipes=recipes)
        else:
            flash('Please log in')
            return redirect(url_for('login'))
    #     handle if account number passed in is not valid object id
    except:
        flash('Please log in')
        return redirect(url_for('login'))


################################################################
# Login Routes
################################################################


'''
GET - Returns the register.html template for new users to register
POST - Accepts the register form and creates a user in the databse, before
redirecting to the login function
'''


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get("email")
        password = request.form.get("password")
        confirmpassword = request.form.get("confirmpassword")
        user = mongo.db.users.find_one({"email": email})

        if user:
            flash('User already exists')
            return redirect(url_for('register'))

        if password != confirmpassword:
            flash('Passwords must match')
            return redirect(url_for('register'))

        new_user = {
            'name': name,
            "email": email,
            "password": generate_password_hash(password),
            "recipes": []
        }
        mongo.db.users.insert_one(new_user)
        added_user = mongo.db.users.find_one({'email': email}, {'_id': 1})

        session['uid'] = str(added_user['_id'])
        flash('Account registered')
        flash('You have been logged in.')
        return redirect(url_for('account', uid=session['uid']))
    return render_template('register.html')


'''
GET - Returns the login.html template for users to input their credentials
POST - Accepts the login form and authenticates the user against the database
before redirecting them to the account template
'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = mongo.db.users.find_one({"email": email})
        if user:
            if check_password_hash(user['password'], password):
                session['uid'] = str(user['_id'])
                flash('You have been logged in.')
                return redirect(url_for('account', uid=session['uid']))
            else:
                flash('Email and password do not match our records')
                return redirect(url_for('login'))
        else:
            flash('Email and password do not match our records')
            return redirect(url_for('login'))

    return render_template('login.html')


'''
GET - Destroys the session and redirects the user to the login template
'''


@app.route('/logout')
def logout():
    session.pop('uid')
    flash('You have been logged out')
    return redirect(url_for('login'))


################################################################
# Cuisine Routes
################################################################


'''
GET - returns the category template populated with a list of cuisines
'''


@app.route('/cuisine')
def cuisine():
    cuisines = list(mongo.db.cuisines.find())
    return render_template('category.html', categories=cuisines,
                           sorting='cuisine', s3_url=s3_url)


'''
GET - Returns the category template populated with recipes based on the
cuisine selection
'''


@app.route('/cuisine/<selection>')
def cuisine_choice(selection):
    recipes = list(mongo.db.recipes.find({'cuisine': selection}))
    return render_template('category.html', categories=recipes,
                           sorting='recipes', endpoint=True, s3_url=s3_url)


################################################################
# Course Routes
################################################################


'''
GET - returns the category template populated with a list of courses
'''


@app.route('/course')
def course():
    courses = list(mongo.db.courses.find())

    return render_template('category.html', categories=courses,
                           sorting='course', s3_url=s3_url)


'''
GET - Returns the category template populated with recipes based on the course
selection
'''


@app.route('/course/<selection>')
def course_choice(selection):
    recipes = list(mongo.db.recipes.find({'course': selection}))
    return render_template('category.html', categories=recipes,
                           sorting='recipes', endpoint=True, s3_url=s3_url)


################################################################
# Surprise Routes
################################################################


'''
GET - Returns a randomly selected recipe using the recipe.html template
'''


@app.route('/surprise')
def surprise():
    recipes = list(mongo.db.recipes.find({}))
    recipe = random.choice(recipes)

    rating_array = recipe['rating']
    if len(rating_array) >= 1:
        average_rating = mean(rating_array)
    else:
        average_rating = 0
    return render_template('recipe.html', recipe=recipe,
                           average_rating=average_rating)


################################################################
# Recipes Routes
################################################################


'''
GET - Returns the recipe template using the selected recipe (from either the
cuisine or course page)
'''


@app.route('/recipes/<selection>/', methods=['GET'])
def recipes_choice(selection):
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(selection)})

    # check to see if this recipe belongs to the logged in user
    users_recipes = mongo.db.users.find_one({'_id': ObjectId(session['uid'])})[
        'recipes']
    if recipe['_id'] in users_recipes:
        recipe_is_mine = True
    else:
        recipe_is_mine = False

    # pull rating for selected recipe
    rating_array = recipe['rating']
    if len(rating_array) >= 1:
        average_rating = mean(rating_array)
    else:
        average_rating = 0

    return render_template('recipe.html', recipe=recipe,
                           average_rating=average_rating,
                           recipe_is_mine=recipe_is_mine)


'''
GET - Returns the edit recipe template for the selected recipe
POST - Updates the record for the selected recipe in the database
'''


@app.route('/recipes/<selection>/edit', methods=['GET', 'POST'])
def edit_recipe(selection):
    # check permission
    current_user = mongo.db.users.find_one({'_id': ObjectId(session['uid'])},
                                           {'recipes': 1})
    if ObjectId(selection) in current_user['recipes']:
        # handle POST request
        if request.method == 'POST':
            form = EditForm()
            if form.validate_on_submit():
                filter = {'_id': ObjectId(selection)}
                update = {
                    'name': request.form['name'],
                    'ingredients': request.form['ingredients'],
                    'instructions': request.form['instructions'],
                    'cuisine': request.form['cuisine'],
                    'course': request.form['course'],
                }
                mongo.db.recipes.update_one(filter, {'$set': update})
                return redirect(url_for('home'))
            else:
                print('rejected')
                return redirect(url_for('home'))
        else:
            # handle GET request

            if ObjectId(selection) in current_user['recipes']:

                recipe = mongo.db.recipes.find_one(
                    {'_id': ObjectId(selection)})
                form = RecipeForm()
                print(form)
                form.name.data = recipe['name']
                form.cuisine.data = recipe['cuisine']
                form.course.data = recipe['course']
                form.ingredients.data = recipe['ingredients']
                form.instructions.data = recipe['instructions']
                return render_template('edit-recipe.html', recipe=recipe,
                                       form=form)
            else:
                flash('You may only edit your own recipes')
                return redirect(url_for('home'))


'''
POST - Deletes the selected recipe in the database and redirects to the home
page
'''


@app.route('/recipes/<selection>/delete', methods=['POST'])
def delete_recipe(selection):
    current_user = mongo.db.users.find_one({'_id': ObjectId(session['uid'])},
                                           {'recipes': 1})
    if ObjectId(selection) in current_user['recipes']:
        mongo.db.recipes.delete_one({'_id': ObjectId(selection)})
        return redirect(url_for('home'))
    else:
        flash('Please log in to delete recipes')
        return redirect(url_for('login'))


'''
NEW RECIPE FORM - Form class for Recipe data model
'''


class RecipeForm(FlaskForm):
    name = StringField('Recipe Name', validators=[DataRequired()],
                       render_kw={'required': True,
                                  'pattern': "^[a-zA-Z]{3,30}$",
                                  'onblur': 'if(isSpacesOnly(this)){alert("Name field must contain characters other than spaces")}'})
    cuisine = SelectField('Cuisine', choices=[('italian', 'Italian'),
                                              ('mexican', 'Mexican'),
                                              ('indian', 'Indian'),
                                              ('french', 'French'),
                                              ('japanese', 'Japanese'),
                                              ('other', 'Other')],
                          validators=[DataRequired()])
    course = SelectField('Course',
                         choices=[('starter', 'Starter'), ('main', 'Main'),
                                  ('dessert', 'Dessert')],
                         validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()],
                                render_kw={'required': True,
                                           'pattern': "^[a-zA-Z0-9).]{3,20}$",
                                           'onblur': 'if(isSpacesOnly(this)){alert("Ingredients field must contain characters other than spaces")}'})
    instructions = TextAreaField('Instructions', validators=[DataRequired()],
                                 render_kw={'required': True,
                                            'pattern': "^[a-zA-Z0-9).]{3,20}$",
                                            'onblur': 'if(isSpacesOnly(this)){alert("Instructions field must contain characters other than spaces")}'})
    image = FileField('Image', validators=[FileRequired(), FileAllowed(
        ['jpg', 'JPG', 'PNG', 'png'])],
                      render_kw={'class': 'file-path validate'})
    submit = SubmitField('Submit', render_kw={'class': 'btn orange darken-4'})


'''
EDIT FORM - Form class for Recipe data model
'''


class EditForm(FlaskForm):
    name = StringField('Recipe Name', validators=[DataRequired()],
                       render_kw={'required': True,
                                  'pattern': "^[a-zA-Z]{3,30}$",
                                  'onblur': 'if(isSpacesOnly(this)){alert("Name field must contain characters other than spaces")}'})
    cuisine = SelectField('Cuisine', choices=[('italian', 'Italian'),
                                              ('mexican', 'Mexican'),
                                              ('indian', 'Indian'),
                                              ('french', 'French'),
                                              ('japanese', 'Japanese'),
                                              ('other', 'Other')],
                          validators=[DataRequired()])
    course = SelectField('Course',
                         choices=[('starter', 'Starter'), ('main', 'Main'),
                                  ('dessert', 'Dessert')],
                         validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()],
                                render_kw={'required': True,
                                           'pattern': "^[a-zA-Z0-9).]{3,20}$",
                                           'onblur': 'if(isSpacesOnly(this)){alert("Ingredients field must contain characters other than spaces")}'})
    instructions = TextAreaField('Instructions', validators=[DataRequired()],
                                 render_kw={'required': True,
                                            'pattern': "^[a-zA-Z0-9).]{3,20}$",
                                            'onblur':
                                                'if(isSpacesOnly(this)){alert("Instructions field must contain characters other than spaces")}'})
    submit = SubmitField('Submit', render_kw={'class': 'btn orange darken-4'})


'''
GET - Returns new-recipe template so users can create a new record
POST - Writes the new record to the database and redirects to the home page
'''


@app.route('/recipes/new-recipe/', methods=['GET', 'POST'])
def new_recipe():
    # handle POST request
    if 'uid' in session:
        form = RecipeForm()
        s3_resource = boto3.resource('s3')
        my_bucket = s3_resource.Bucket(os.environ.get('BUCKET_NAME'))
        if request.method == 'POST':
            if form.validate_on_submit():
                image = request.files['image']
                filename = secrets.token_hex(8)
                my_bucket.Object(filename).put(Body=image)
                new_recipe = {
                    'name': request.form['name'],
                    'ingredients': request.form['ingredients'],
                    'instructions': request.form['instructions'],
                    'rating': [],
                    'cuisine': request.form['cuisine'],
                    'course': request.form['course'],
                    'image': filename,
                }
                inserted_recipe = mongo.db.recipes.insert_one(new_recipe)
                mongo.db.users.update_one({'_id': ObjectId(session['uid'])},
                                          {'$addToSet': {
                                              'recipes': inserted_recipe.inserted_id}})
                print('inserted')
                return redirect(url_for('home'))
            else:
                print('rejected')
        else:
            # handle GET request
            return render_template('new-recipe.html', form=form,
                                   my_bucket=my_bucket)
    else:
        flash('Please log in to create recipes')
        return redirect(url_for('login'))


'''
POST Adds the users rating to the record and redirects to the home page
'''


@app.route('/recipes/<selection>/rating', methods=['POST'])
def rate_recipe(selection):
    rating = request.form.get('rating')
    recipe_url = request.form.get('recipe_url')
    print(rating)
    print(selection)
    mongo.db.recipes.update_one({'_id': ObjectId(selection)},
                                {'$addToSet': {'rating': int(rating)}})
    flash('rating submitted')
    return redirect(url_for('recipes_choice', selection=selection))


################################################################
# Run Server
################################################################
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)
