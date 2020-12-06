#  Copyright (c) 2020. Bryan S Mullen. All rights reserved.
import os
from flask import Flask, flash, render_template, redirect, request, session, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
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
            "email": email,
            "password": generate_password_hash(password)
        }
        mongo.db.users.insert_one(new_user)

        session['user'] = email
        flash('Account registered')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = mongo.db.users.find_one({"email": email})

        if user:
            if check_password_hash(user['password'], password):
                session['user'] = email
                flash('You have been logged in.')
            else:
                flash('Email and password do not match our records')
                return redirect(url_for('login'))
        else:
            flash('Email and password do not match our records')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    recipes = mongo.db.recipes.find()
    return render_template('recipes.html', recipes=recipes)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
# TODO: REMOVE DEBUG=True BEFORE PRODUCTION. ONLY ADDED AT THIS STAGE IN COMPLIANCE WITH TAUGHT MATERIAL PROVIDED BY CODE INSTITUTE