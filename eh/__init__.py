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

# Import APScheduler assets and configure scheduler.
from apscheduler.scheduler import Scheduler
from apscheduler.jobstores.ram_store import RAMJobStore

# Initialize the scheduler, scrubs jobs, start.
sched = Scheduler()
sched.add_jobstore(RAMJobStore(), 'slicers')
for job in sched.get_jobs(): sched.unschedule_job(job)
sched.start()

# Import application assets.
from eh.views import admin
