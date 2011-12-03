from flask import Flask
import datetime

# Create Flask application.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
app.permanent_session_lifetime = datetime.timedelta(minutes = 10)

# Import and set the session key.
import key
app.secret_key = key.secret

# Import SQLAlchemy and initialize the database object.
from flaskext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Import application assets.
from eh.views import admin
