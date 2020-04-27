from flask import flash
from mysqlconnection import connectToMySQL
from config import bcrypt, re, EMAIL_REGEX, PWD_REGEX, socketio
from flask_socketio import SocketIO

mySQLdb = "project-card-room1"
starting_balance = 10000  

def addUser(user_name, email, password, confirm):
    user_added = False
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
        else:
            # add new member
            mySQL = connectToMySQL(mySQLdb)
            query = "INSERT INTO users (user_name, email, password, balance, created_at, updated_at) VALUES (%(un)s, %(em)s, %(pwd)s, %(b)s, NOW(), NOW());"
            data = {
                'un': user_name,
                'em': email,
                'pwd': bcrypt.generate_password_hash(password),
                'b': starting_balance
            }
            mySQL.query_db(query, data)
            flash("New user added.")
            user_added = True
    return user_added

def loginUser(email, password):
    user_id = False
    mySQL = connectToMySQL(mySQLdb)
    query = "SELECT id, password FROM users WHERE email = %(em)s;"
    data = {
        'em': email
    }
    result = mySQL.query_db(query, data)
    if result:
        if bcrypt.check_password_hash(result[0]['password'], password):
            user_id = result[0]['id']
        else:
            flash("Login failed.")
    else:
        flash("Unknown user.")
    return user_id

def getUser(user_id):
    # get user info from user_id
    # returns user info (id, user_name, balance, photo) in the form of a dictonary
    # returns False if user not registered
    # TO DO will need to update to get win/loss record from games_players table
    mySQL = connectToMySQL(mySQLdb)
    query = "SELECT id, user_name, email, balance, photo FROM users WHERE id = %(id)s;"
    data = {
        'id': user_id
    }
    result = mySQL.query_db(query, data)
    if result:
        return result[0]  # return user info
    else:
        return False  # user not in database

def getActiveGames():
    # get game info for all active games, i.e. with game_status == 0 or 1
    # game_status: 0 if waiting, 1 if playing, 2 if completed
    # returns game info (game_id, game_status, pot, game_name, time_limit, min_players, max_players, ante, max_raise) in the form of an array of dictionaries
    mySQL = connectToMySQL(mySQLdb)
    query = "SELECT games.id as game_id, game_status, pot, game_name, time_limit, min_player, max_player, ante, max_raise FROM games JOIN game_types ON game_types.id = games.id WHERE game_status = 0 OR game_status = 1;"
    result = mySQL.query_db(query)
    return result  # return game info

def joinGame(user, game_id):
    return False

def getGameIDFromUserID(user_id):
    return 1

def getGame(game_id):
    # get game info for game_id
    # returns game info in tuple of (game, players)
    # game is (game_id, game_status, pot, game_name, time_limit, min_players, max_players, ante, max_raise) in the form a dictionary
    # players is (user_id, user_name, balance, photo) in the form of an array of dictionaries 
    game = {}
    game['game_id'] = 1
    game['game_status'] = 1
    game['pot'] = 200
    game['game_name'] = '5-Card Stud'
    game['time_limit'] = 30
    game['turn'] = 0
    game['num_players'] = 4
    game['min_players'] = 4
    game['max_players'] = 4
    game['ante'] = 10
    game['max_raise'] = 50
    players = [{},{},{}]
    players[0] = {}
    players[0]['user_id'] = 1
    players[0]['user_name'] = "Mary"
    players[0]['balance'] = 7000
    players[0]['photo'] = False
    players[0]['message'] = 'Hi All!'
    players[0]['cards'] = [{},{},{},{},{}]
    players[0]['cards'][0] = {'number': 5, 'suit': 1, 'face_up': 1}
    players[0]['cards'][1] = {'number': 10, 'suit': 1, 'face_up': 1}
    players[0]['cards'][2] = {'number': 1, 'suit': 2, 'face_up': 0}
    players[0]['cards'][3] = {'number': 7, 'suit': 3, 'face_up': 0}
    players[0]['cards'][4] = {'number': 11, 'suit': 4, 'face_up': 0}
    players[1] = {}
    players[1]['user_id'] = 2
    players[1]['user_name'] = "Joe"
    players[1]['balance'] = 5000
    players[1]['photo'] = False
    players[1]['message'] = 'Hi!'
    players[1]['cards'] = [{},{},{},{}]
    players[1]['cards'][0] = {'number': 11, 'suit': 1, 'face_up': 1}
    players[1]['cards'][1] = {'number': 12, 'suit': 2, 'face_up': 1}
    players[1]['cards'][2] = {'number': 1, 'suit': 1, 'face_up': 1}
    players[1]['cards'][3] = {'number': 6, 'suit': 4, 'face_up': 0}
    players[2] = {}
    players[2]['user_id'] = 3
    players[2]['user_name'] = "Elizabeth"
    players[2]['balance'] = 3000
    players[2]['photo'] = False
    players[2]['message'] = "Hey losers!"
    players[2]['cards'] = [{},{},{},{},{}]
    players[2]['cards'][0] = {'number': 3, 'suit': 1, 'face_up': 1}
    players[2]['cards'][1] = {'number': 5, 'suit': 2, 'face_up': 1}
    players[2]['cards'][2] = {'number': 1, 'suit': 2, 'face_up': 0}
    players[2]['cards'][3] = {'number': 1, 'suit': 3, 'face_up': 0}
    players[2]['cards'][4] = {'number': 1, 'suit': 4, 'face_up': 0}
    return game, players

def startNewGame(user, game_type_id):
    
    return False

def getTopWinLossRecords(num_of_players):
    return False

def getTopBettors(num_of_players):
    return False

def gameFold(user, game_id):
    return False

def gameCall(user, game_id):
    return False

def gameRaise(user, game_id, raise_amount):
    return False

def gameMessage(user, game_id, message):
    return False
