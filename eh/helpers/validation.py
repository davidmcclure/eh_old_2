'''
Validation logic.
'''

import eh.models as models
from eh.lib.messages import errors as e


def validateAdminRegistration(
        username,
        password,
        confirm):

    ''' Validate a new administrator. '''

    is_error = False
    errors = {}
    errors['_form'] = []
    errors['username'] = []
    errors['password'] = []
    errors['confirm'] = []

    # Username present?
    if not username:
        errors['username'].append(e['noUsername'])
        is_error = True

    # Username available?
    elif not models.User.userNameAvailable(username):
        errors['username'].append(e['usernameTaken'])
        is_error = True

    # Password present?
    if not password:
        errors['password'].append(e['noPassword'])
        is_error = True

    # Password confirm present?
    if not confirm:
        errors['confirm'].append(e['noConfirm'])
        is_error = True

    # Password and confirmation match?
    elif password != confirm:
        errors['confirm'].append(e['confirmDoesNotMatch'])
        is_error = True

    if not is_error: errors = None

    return errors


def validateAdminLogin(
        username,
        password):

    ''' Validate an admin login attempt. '''

    is_error = False
    errors = {}
    errors['_form'] = []
    errors['username'] = []
    errors['password'] = []

    # Username present?
    if not username:
        errors['username'].append(e['noUsername'])
        is_error = True

    # Password present?
    if not password:
        errors['password'].append(e['noPassword'])
        is_error = True

    # Username and password valid?
    if username and password:

        # Try to find a user.
        admin = models.User.getUserByName(username)

        # No user with supplied name?
        if not admin:
            errors['username'].append(e['usernameDoesNotExist'])
            is_error = True

        # Not an administrator?
        elif not admin.is_admin:
            errors['_form'].append(e['notAuthorized'])
            is_error = True

        # Wrong password?
        elif not admin.checkPassword(password):
            errors['password'].append(e['incorrectPassword'])
            is_error = True

    if not is_error: errors = None

    return errors
