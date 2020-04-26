from flask import Flask
import re  # the regex module    
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PWD_REGEX = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!*#?&])[A-Za-z\d@$!#*?&]{6,20}$")
app = Flask(__name__)
app.secret_key = "bbbafdskiezxfjopterwggggfdsafdsafsdawiofxxgf"
bcrypt = Bcrypt(app)    # we are creating an object called bcrypt, 
                        # which is made by invoking the function Bcrypt with our app as an argument
socketio = SocketIO(app)
