from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
from config import bcrypt, re, EMAIL_REGEX, PWD_REGEX, socketio
from flask_socketio import SocketIO

mySQLdb = "project_card_room1"
starting_balance = 500   

def login_registration():
    return render_template('login-registration.html')

def login_action():
    mySQL = connectToMySQL(mySQLdb)
    query = "SELECT id, password FROM users WHERE email = %(em)s;"
    data = {
        'em': request.form['email']
    }
    result = mySQL.query_db(query, data)
    if result:
        if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
            session['memberid'] = result[0]['id']
            return redirect('/user-profile')  # successful login
        else:
            flash("Login failed.")
    else:
        flash("Unknown user.")
    return redirect('/login-registration')

def registration_action():
    user_name = request.form['user_name']
    email = request.form['email']
    password = request.form['password']
    confirm = request.form['confirm']
    if len(user_name) == 0:
        flash("Please enter user name.")
    elif not EMAIL_REGEX.match(email):    # test whether a field matches the pattern
        flash("Invalid email address.")
    elif not re.search(PWD_REGEX, password): 
        flash("Password must be 6-20 characters and contain one or more of each of: a number, uppercase letter, lower case letter, and special symbol.")
    elif password != confirm:
        flash("Password confirmation does not match.")
    else: 
        # check if email address already exists
        mySQL = connectToMySQL(mySQLdb)
        query = "SELECT id FROM users WHERE name = %(em)s;"
        data = {
            'em': email
        }
        result = mySQL.query_db(query, data)
        if result:
            flash("Account already exists.")
            return redirect('/login-registration')
        # add new member
        mySQL = connectToMySQL(mySQLdb)
        query = "INSERT INTO users (user_name, email, password, balance, wins, losses, created_at, updated_at) VALUES (%(un)s, %(em)s, %(pwd)s, %(b)s, %(w)s, %(l)s, NOW(), NOW());"
        data = {
            'un': user_name,
            'em': email,
            'pwd': bcrypt.generate_password_hash(password),
            'b': starting_balance,
            'w': 0,  # no wins
            'l': 0   # no losses
        }
        mySQL.query_db(query, data)
        flash("New user added.")
    return redirect('/login-registration')

def logout_action():
    session.clear()
    flash("Logged out.")
    return redirect('/login-registration')
