from flask import Flask
import datetime

# Create Flask application.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memory'
app.permanent_session_lifetime = datetime.timedelta(minutes = 10)

# Import and set the session key.
import key
app.secret_key = key.secret

# Import SQLAlchemy and initialize the database object.
from flaskext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Run the scheduler.
from eh.helpers.scheduler import HaikuScheduler
sched = HaikuScheduler()
sched.start()

# Import application assets.
from eh.views import admin
