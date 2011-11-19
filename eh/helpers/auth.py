'''
Authorization view decorators.
'''

from flask import request, Response, redirect, url_for, session
import eh.models as models
from functools import wraps


def requiresAdmin(f):

    ''' Is there at least one administrator? '''

    @wraps(f)
    def decorated(*args, **kwargs):
        if not models.User.administratorExists():
            return redirect(url_for('register'))
        return f(*args, **kwargs)
    return decorated


def requiresAdminLogin(f):

    ''' Is the user an administrator and logged in? '''

    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' in session:
            id = session['user_id']
            if models.User.userIsAdmin(id): return f(*args, **kwargs)
            else: return redirect(url_for('logout'))
        else:
            session['login_target'] = request.script_root
            return redirect(url_for('login'))
    return decorated


def requiresAdminNoLogin(f):

    ''' Is the user not logged in? '''

    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('browse'))
    return decorated


def requiresNoAdmin(f):

    ''' Are there no administrators? '''

    @wraps(f)
    def decorated(*args, **kwargs):
        if models.User.administratorExists():
            return redirect(url_for('login'))
        else:
            return f(*args, **kwargs)
    return decorated
