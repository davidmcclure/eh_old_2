'''
Administrative views. Create, start, stop, and delete poems.
'''

# Get application assets.
from flask import session, redirect, url_for, request, render_template
from eh import app, db
from eh.helpers import auth


@app.route('/admin')
@auth.requiresAdmin
@auth.requiresAdminLogin
def browse():

    ''' Create and run haiku. '''

    return '/admin'


@app.route('/admin/register', methods=['GET', 'POST'])
@auth.requiresNoAdmin
def register():

    ''' First admin registration. '''

    return '/admin/register'


@app.route('/admin/login', methods=['GET', 'POST'])
@auth.requiresAdmin
@auth.requiresAdminNoLogin
def login():

    ''' Admin login. '''

    return '/admin/login'


@app.route('/admin/logout')
def logout():

    ''' Admin logout. '''

    session.pop('user_id', None)
    return redirect(url_for('login'))
