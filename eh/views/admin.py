'''
Administrative views. Create, start, stop, and delete poems.
'''

# Get application assets.
from flask import session, redirect, url_for, request, render_template
from eh import app, db
from eh.helpers import auth, validation
import eh.models as models


@app.route('/admin')
@auth.isInstalled
@auth.isAdmin
def browse():

    ''' Create and run haiku. '''

    return render_template('admin/browse.html')


@app.route('/admin/new', methods=['GET', 'POST'])
@auth.isInstalled
@auth.isAdmin
def new():

    ''' Create a new haiku. '''

    errors = None

    # If a form was posted.
    if request.method == 'POST':

        # Gather post.
        title =             request.form['title']
        slug =              request.form['url_slug']
        roundLength =       request.form['word_round_length']
        interval =          request.form['slicing_interval']
        minSubmissions =    request.form['min_blind_submissions']
        submissionValue =   request.form['blind_submission_value']
        halfLife =          request.form['decay_half_life']
        capital =           request.form['seed_capital']

        # Validate form.
        errors = validation.validateHaiku(
                title,
                slug,
                roundLength,
                interval,
                minSubmissions,
                submissionValue,
                halfLife,
                capital)

        # If valid.
        if not errors:

            # Create the administrator.
            haiku = models.Haiku.createHaiku(
                    title,
                    slug,
                    round_length,
                    interval,
                    min_submissions,
                    submission_value,
                    half_life,
                    capital)

            # Record the id, redirect.
            return redirect(url_for('browse'))

    return render_template(
            'admin/new.html',
            errors = errors,
            form = request.form)


@app.route('/admin/register', methods=['GET', 'POST'])
@auth.isNotInstalled
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
@auth.isInstalled
@auth.isNotAdmin
def login():

    ''' Admin login. '''

    errors = None

    # If a form was posted.
    if request.method == 'POST':

        # Gather post.
        username = request.form['username']
        password = request.form['password']

        # Validate form.
        errors = validation.validateAdminLogin(
                username,
                password)

        # If valid.
        if not errors:

            # Get the user record.
            admin = models.User.getUserByName(username)

            # Record the id, redirect.
            session['user_id'] = admin.id
            return redirect(url_for('browse'))

    return render_template(
            'admin/login.html',
            errors = errors,
            form = request.form)


@app.route('/admin/logout')
@auth.isInstalled
def logout():

    ''' Admin logout. '''

    session.pop('user_id', None)
    return redirect(url_for('login'))
