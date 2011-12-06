'''
Form scrubbers.
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
    elif models.User.getUserByName(username):
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


def validateHaiku(
        slug,
        roundLength,
        interval,
        minSubmissions,
        submissionValue,
        halfLife,
        capital):

    ''' Validate a haiku. '''

    is_error = False
    errors = {}
    errors['_form'] = []
    errors['url_slug'] = []
    errors['word_round_length'] = []
    errors['slicing_interval'] = []
    errors['min_blind_submissions'] = []
    errors['blind_submission_value'] = []
    errors['decay_half_life'] = []
    errors['seed_capital'] = []

    # Slug present?
    if not slug:
        errors['url_slug'].append(e['noSlug'])
        is_error = True

    # Slug taken?
    if models.Haiku.getHaikuBySlug(slug):
        errors['url_slug'].append(e['slugTaken'])
        is_error = True

    # Round length present?
    if not roundLength:
        errors['word_round_length'].append(e['noRoundLength'])
        is_error = True

    # Round length an integer?
    else:
        try: int(roundLength)
        except ValueError:
            errors['word_round_length'].append(e['mustBeInt'])
            is_error = True

    # Slicing interval present?
    if not interval:
        errors['slicing_interval'].append(e['noInterval'])
        is_error = True

    # Slicing interval an integer?
    else:
        try: int(interval)
        except ValueError:
            errors['slicing_interval'].append(e['mustBeInt'])
            is_error = True

    # Minimum blind submissions present?
    if not minSubmissions:
        errors['min_blind_submissions'].append(e['noMinSubmissions'])
        is_error = True

    # Minimum blind submissions an integer?
    else:
        try: int(minSubmissions)
        except ValueError:
            errors['min_blind_submissions'].append(e['mustBeInt'])
            is_error = True

    # Blind submission value present?
    if not submissionValue:
        errors['blind_submission_value'].append(e['noSubmissionValue'])
        is_error = True

    # Blind submission value an integer?
    else:
        try: int(submissionValue)
        except ValueError:
            errors['blind_submission_value'].append(e['mustBeInt'])
            is_error = True

    # Half-life value present?
    if not halfLife:
        errors['decay_half_life'].append(e['noHalfLife'])
        is_error = True

    # Half life an integer?
    else:
        try: int(halfLife)
        except ValueError:
            errors['decay_half_life'].append(e['mustBeInt'])
            is_error = True

    # Seed capital present?
    if not capital:
        errors['seed_capital'].append(e['noCapital'])
        is_error = True

    # Seed capital an integer?
    else:
        try: int(capital)
        except ValueError:
            errors['seed_capital'].append(e['mustBeInt'])
            is_error = True

    if not is_error: errors = None

    return errors
