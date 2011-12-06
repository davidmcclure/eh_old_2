'''
Authorization view decorators.
'''

from flask import request, Response, redirect, url_for, session
import eh.models as models
from functools import wraps

def isAdmin(f):

    ''' If there is a logged-in administrator. '''

    @wraps(f)
    def decorated(*args, **kwargs):

        # If no user_id in the session, redirect to login.
        if 'user_id' not in session:
            return redirect(url_for('login'))

        # If the user is an administrator, pass the user object into
        # the method; otherwise, redirect to login.
        else:

            # Get the id.
            id = session['user_id']

            # If admin, pass user object.
            if models.User.userIsAdmin(id):
                admin = models.User.query.get(id)
                kwargs['admin'] = admin
                return f(*args, **kwargs)

            else: return redirect(url_for('login'))

    return decorated


def isNotAdmin(f):

    ''' If there is not a logged-in administrator. '''

    @wraps(f)
    def decorated(*args, **kwargs):

        # If no user_id in the session, redirect to login.
        if 'user_id' not in session:
            return f(*args, **kwargs)

        # If the user is an administrator, execute the browse method;
        # otherwise, redirect to login
        else:

            # Get the id.
            id = session['user_id']

            # If admin, redirect to browse.
            if models.User.userIsAdmin(id):
                return redirect(url_for('browse'))
            else:
                return f(*args, **kwargs)

    return decorated


def isInstalled(f):

    ''' If the application has been installed. '''

    @wraps(f)
    def decorated(*args, **kwargs):

        # Check for administrators in the database.
        if models.User.userExists():
            return f(*args, **kwargs)

        # If no administrators, redirect to register.
        else:
            return redirect(url_for('register'))

    return decorated


def isNotInstalled(f):

    ''' If the application has not been installed. '''

    @wraps(f)
    def decorated(*args, **kwargs):

        # Check for no administrators in the database.
        if not models.User.userExists():
            return f(*args, **kwargs)

        else:
            return redirect(url_for('admin'))

    return decorated
