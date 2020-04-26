from flask import Flask, render_template, request, redirect, session
from utilities import *


def login_registration():
    session.clear()
    return render_template('login-registration.html')

def login_action():
    email = request.form['email']
    password = request.form['password']
    user_id = loginUser(email, password)
    if id:
        session['memberid'] = user_id
        return redirect('/user-profile')
    else:
        return redirect('/login-registration')

def registration_action():
    user_name = request.form['user_name']
    email = request.form['email']
    password = request.form['password']
    confirm = request.form['confirm']
    addUser(user_name, email, password, confirm)
    return redirect('/login-registration')

def user_profile():
    if 'user_id' in session:
        user_id = session['user_id']
        user = getUser(user_id)
        if user:
            return render_template('user_profile.html', user = user)
    return redirect('/login-registration')

def lobby():
    if 'user_id' in session:
        user_id = session['user_id']
        user = getUser(user_id)
        if user:
            games = getActiveGames()
            return render_template('lobby.html', user = user, games = games)
    return redirect('/login-registration')

def card_table():
    # if 'user_id' in session:
    #     user_id = session['user_id']
    #     user = getUser(user_id)
    #     if user:
    game_id = getGameIDFromUserID(user_id=1)
    game, players = getGame(game_id)
    user = {}
    if game:
        return render_template('card-table.html', user = user, game = game, players = players)
    else:
        return redirect('/lobby')

def leaderboard():
    records = getTopWinLossRecords(10)
    bettors = getTopBettors(10)
    return render_template('leaderboard.html', records = records, bettors = bettors)

def logout_action():
    session.clear()
    flash("Logged out.")
    return redirect('/login-registration')
