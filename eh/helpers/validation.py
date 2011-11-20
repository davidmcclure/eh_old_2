'''
Validation logic.
'''

from flask import request, session
import eh.models as models
from werkzeug.security import check_password_hash
import re


def validateAdminRegistration(
        username,
        password,
        confirm):

    ''' Validate a user. '''

    is_error = False
    errors = {}
    errors['_form'] = []
    errors['username'] = []
    errors['password'] = []
    errors['confirm'] = []

    # Username present?
    if not username:
        errors['username'].append('Enter a username.')
        is_error = True

    # Username available?
    elif not models.User.userNameAvailable(username):
        errors['username'].append('Username taken.')
        is_error = True

    # Password present?
    if not password:
        errors['password'].append('Enter a password.')
        is_error = True

    # Password confirm present?
    if not confirm:
        errors['confirm'].append('Confirm your password.')
        is_error = True

    # Password and confirmation match?
    elif password != confirm:
        errors['confirm'].append('Does not match.')
        is_error = True

    if not is_error: errors = None

    return errors
