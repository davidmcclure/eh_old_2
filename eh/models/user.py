'''
The user model for administrators and participants.
'''

# Get application assets.
from eh import app, db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime as dt


class User(db.Model):

    ''' Participants and administrators. '''

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password_hash = db.Column(db.String(60))
    is_admin = db.Column(db.Boolean, default=False)


    # Row methods:

    def __init__(self, username, password, admin):

        ''' Set username, generate password hash. '''

        self.username = username
        self.is_admin = admin
        self.setPassword(password)


    def setPassword(self, password):

        ''' Generate hash from password, set. '''

        self.password_hash = generate_password_hash(password)
