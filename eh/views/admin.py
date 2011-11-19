'''
Administrative views. Create, start, stop, and delete poems.
'''

# Get application assets.
from flask import session, redirect, url_for, request, render_template
from eh import app, db

@app.route('/admin')
def browse():

    ''' Create and run haiku. '''

    return '/admin'
