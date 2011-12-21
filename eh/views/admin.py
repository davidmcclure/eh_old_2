'''
Administrative views. Create, start, stop, and delete poems.
'''

# Get application assets.
from flask import session, redirect, url_for, request, render_template
from eh import app, db, sched
from eh.helpers import auth, validation, slicer
import eh.models as models


@app.route('/admin')
@auth.isInstalled
@auth.isAdmin
def browse(admin):

    ''' Create and run haiku. '''

    # Get all haiku.
    haiku = models.Haiku.query.all()

    return render_template(
            'admin/browse.html',
            haiku = haiku,
            sched = sched)


@app.route('/admin/new', methods=['GET', 'POST'])
@auth.isInstalled
@auth.isAdmin
def new(admin):

    ''' Create a new haiku. '''

    errors = None

    # If a form was posted.
    if request.method == 'POST':

        # Gather post.
        slug =              request.form['url_slug']
        roundLength =       request.form['word_round_length']
        interval =          request.form['slicing_interval']
        minSubmissions =    request.form['min_blind_submissions']
        submissionValue =   request.form['blind_submission_value']
        halfLife =          request.form['decay_half_life']
        capital =           request.form['seed_capital']

        # Validate form.
        errors = validation.validateHaiku(
                slug,
                roundLength,
                interval,
                minSubmissions,
                submissionValue,
                halfLife,
                capital)

        # If valid.
        if not errors:

            # Create the haiku.
            haiku = models.Haiku.createHaiku(
                    admin.id,
                    slug,
                    roundLength,
                    interval,
                    minSubmissions,
                    submissionValue,
                    halfLife,
                    capital)

            # Record the id, redirect.
            return redirect(url_for('browse'))

    return render_template(
            'admin/new.html',
            errors = errors,
            form = request.form)


@app.route('/admin/start/<id>')
@auth.isInstalled
@auth.isAdmin
def start(admin, id):

    ''' Start a haiku. '''

    # Get the record, start the slicer.
    haiku = models.Haiku.query.get(id)
    sched.createSlicer(haiku, slicer.slice)

    return redirect(url_for('browse'))


@app.route('/admin/stop/<id>')
@auth.isInstalled
@auth.isAdmin
def stop(admin, id):

    ''' Stop a haiku. '''

    # Get the record, stop the slicer.
    haiku = models.Haiku.query.get(id)
    sched.deleteSlicer(haiku)

    return redirect(url_for('browse'))


@app.route('/admin/delete/<id>')
@auth.isInstalled
@auth.isAdmin
def delete(admin, id):

    ''' Delete a haiku. '''

    models.Haiku.deleteHaiku(id)

    return redirect(url_for('browse'))


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
