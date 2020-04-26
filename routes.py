from config import app
from controller_functions import *

app.add_url_rule('/', view_func=login_registration)
app.add_url_rule('/login-registration', view_func=login_registration)
app.add_url_rule('/login-action', view_func=login_action, methods=['POST'])
app.add_url_rule('/registration-action', view_func=registration_action, methods=['POST'])

app.add_url_rule('/logout-action', view_func=logout_action)

