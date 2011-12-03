'''
Administrative views. Create, start, stop, and delete poems.
'''

# Get application assets.
from flask import session, redirect, url_for, request, render_template
from eh import app, db
from eh.helpers import auth, validation
import eh.models as models


@app.route('/admin')
@auth.requiresAdmin
@auth.requiresAdminLogin
def browse():

    ''' Create and run haiku. '''

    return render_template('admin/browse.html')


@app.route('/admin/new', methods=['GET', 'POST'])
@auth.requiresAdmin
@auth.requiresAdminLogin
def new():

    ''' Create a new haiku. '''

    return '/admin/new'


@app.route('/admin/register', methods=['GET', 'POST'])
@auth.requiresNoAdmin
def register():

    ''' First admin registration. '''

    errors = None

    # If a form was posted.
    if request.method == 'POST':

        # Gather post.
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']

        # Validate form.
        errors = validation.validateAdminRegistration(
                username,
                password,
                confirm)

        # If valid.
        if not errors:

            # Create the administrator.
            admin = models.User.createAdministrator(
                    username,
                    password)

            # Record the id, redirect.
            session['user_id'] = admin.id
            return redirect(url_for('browse'))

    # If not valid, render form again.
    return render_template(
            'admin/register.html',
            errors = errors,
            form = request.form)


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
