'''
Unit tests for validation helpers.
'''

from eh import app, db
from werkzeug.security import check_password_hash
from eh.models import User
from eh.helpers import validation
from eh.lib.messages import errors as e
import UnitTestCase as u


class ValidateAdminRegistrationUnitTest(u.UnitTestCase):


    def testValidParameters(self):

        ''' Valid parameters should pass the checks. '''

        errors = validation.validateAdminRegistration(
                'username',
                'password',
                'password')

        # Errors should be None.
        self.assertIsNone(errors)


    def testNoUserName(self):

        ''' Empty or blank username should throw an error. '''

        # Blank username.
        errors = validation.validateAdminRegistration(
                '',
                'password',
                'password')

        # Check for error.
        self.assertEqual(errors['username'], [e['noUsername']])

        # None username.
        errors = validation.validateAdminRegistration(
                None,
                'password',
                'password')

        # Check for error.
        self.assertEqual(errors['username'], [e['noUsername']])


    def testUsernameUnavailable(self):

        ''' Already registered username should throw an error. '''

        # Create an administrator.
        takenUsername = User('takenUsername', 'password', True)
        db.session.add(takenUsername)
        db.session.commit()

        # Taken username.
        errors = validation.validateAdminRegistration(
                'takenUsername',
                'password',
                'password')

        # Check for error.
        self.assertEqual(errors['username'], [e['usernameTaken']])


    def testNoPassword(self):

        ''' Empty or blank password should throw an error. '''

        # Blank password.
        errors = validation.validateAdminRegistration(
                'username',
                '',
                'password')

        # Check for error.
        self.assertEqual(errors['password'], [e['noPassword']])

        # None password.
        errors = validation.validateAdminRegistration(
                'username',
                None,
                'password')

        # Check for error.
        self.assertEqual(errors['password'], [e['noPassword']])


    def testNoConfirm(self):

        ''' Empty or blank password confirm should throw an error. '''

        # Blank confirm.
        errors = validation.validateAdminRegistration(
                'username',
                'password',
                '')

        # Check for error.
        self.assertEqual(errors['confirm'], [e['noConfirm']])

        # None password.
        errors = validation.validateAdminRegistration(
                'username',
                'password',
                None)

        # Check for error.
        self.assertEqual(errors['confirm'], [e['noConfirm']])


    def testConfirmMatch(self):

        ''' If the confirmation does not match the password, throw an error. '''

        # Mismatch.
        errors = validation.validateAdminRegistration(
                'username',
                'password',
                'nomatch')

        # Check for error.
        self.assertEqual(errors['confirm'], [e['confirmDoesNotMatch']])



if __name__ == '__main__':
    u.unittest.main()
