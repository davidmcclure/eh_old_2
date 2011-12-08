'''
Unit tests for validation helpers.
'''

from eh import app, db
from werkzeug.security import check_password_hash
from eh.models import User, Haiku
from eh.helpers import validation
from eh.lib.messages import errors as e
import UnitTestCase as u


class ValidateAdminRegistrationUnitTest(u.UnitTestCase):


    def testValidParameters(self):

        '''
        Valid parameters should pass the checks.
        '''

        errors = validation.validateAdminRegistration(
                'username',
                'password',
                'password')

        # Errors should be None.
        self.assertIsNone(errors)


    def testNoUserName(self):

        '''
        Empty or blank username should throw an error.
        '''

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

        '''
        Already registered username should throw an error.
        '''

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

        '''
        Empty or blank password should throw an error.
        '''

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

        '''
        Empty or blank password confirm should throw an error.
        '''

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

        '''
        If the confirmation does not match the password, throw an error.
        '''

        # Mismatch.
        errors = validation.validateAdminRegistration(
                'username',
                'password',
                'nomatch')

        # Check for error.
        self.assertEqual(errors['confirm'], [e['confirmDoesNotMatch']])



class ValidateAdminLoginUnitTest(u.UnitTestCase):


    def setUp(self):

        '''
        Create user and administrator records to test against.
        '''

        super(ValidateAdminLoginUnitTest, self).setUp()

        admin = User.createAdministrator('adminname', 'password')
        user = User.createUser('username', 'password')


    def testValidParameters(self):

        '''
        Valid parameters should pass.
        '''

        errors = validation.validateAdminLogin(
                'adminname',
                'password')

        # Errors should be None.
        self.assertIsNone(errors)


    def testNoUserName(self):

        '''
        Empty or blank username.
        '''

        # Blank username.
        errors = validation.validateAdminLogin(
                '',
                'password')

        # Check for error.
        self.assertEqual(errors['username'], [e['noUsername']])

        # None username.
        errors = validation.validateAdminLogin(
                None,
                'password')

        # Check for error.
        self.assertEqual(errors['username'], [e['noUsername']])


    def testNoPassword(self):

        '''
        Empty or blank password.
        '''

        # Blank username.
        errors = validation.validateAdminLogin(
                'adminname',
                '')

        # Check for error.
        self.assertEqual(errors['password'], [e['noPassword']])

        # None password.
        errors = validation.validateAdminLogin(
                'adminname',
                None)

        # Check for error.
        self.assertEqual(errors['password'], [e['noPassword']])


    def testNonExistentUserName(self):

        '''
        Nonexistent username.
        '''

        # Non-existent username.
        errors = validation.validateAdminLogin(
                'doesnotexist',
                'password')

        # Check for error.
        self.assertEqual(errors['username'], [e['usernameDoesNotExist']])


    def testNotAdministrator(self):

        '''
        Valid user account that is not an admin.
        '''

        # Non-admin.
        errors = validation.validateAdminLogin(
                'username',
                'password')

        # Check for error.
        self.assertEqual(errors['_form'], [e['notAuthorized']])


    def testWrongPassword(self):

        '''
        Existing admin username with incorrect password.
        '''

        # Non-admin.
        errors = validation.validateAdminLogin('adminname', 'wrong')

        # Check for error.
        self.assertEqual(errors['password'], [e['incorrectPassword']])



class ValidateHaikuUnitTest(u.UnitTestCase):


    def setUp(self):

        '''
        Create existing haiku record to test against.
        '''

        super(ValidateHaikuUnitTest, self).setUp()

        admin = User.createAdministrator('username', 'password')
        haiku = Haiku.createHaiku(admin.id, 'slug', 1000, 1, 5, 100, 20, 1000)


    def testValidParameters(self):

        '''
        Valid parameters should pass.
        '''

        errors = validation.validateHaiku('newslug', 1000, 1, 5, 100, 20, 1000)

        # Errors should be None.
        self.assertIsNone(errors)


    def testNoSlug(self):

        '''
        Empty or blank slug.
        '''

        # Blank slug.
        errors = validation.validateHaiku('', 1000, 1, 5, 100, 20, 1000)

        # Check for error.
        self.assertEqual(errors['url_slug'], [e['noSlug']])

        # None slug.
        errors = validation.validateHaiku(None, 1000, 1, 5, 100, 20, 1000)

        # Check for error.
        self.assertEqual(errors['url_slug'], [e['noSlug']])


    def testTakenSlug(self):

        '''
        Slug already taken.
        '''

        # Taken slug.
        errors = validation.validateHaiku('slug', 1000, 1, 5, 100, 20, 1000)

        # Check for error.
        self.assertEqual(errors['url_slug'], [e['slugTaken']])


    def testNoRoundLength(self):

        '''
        Empty round length.
        '''

        # None round length.
        errors = validation.validateHaiku('newslug', None, 1, 5, 100, 20, 1000)

        # Check for error.
        self.assertEqual(errors['word_round_length'], [e['noRoundLength']])


    def testNonIntRoundLength(self):

        '''
        Non-integer round length.
        '''

        # String round length.
        errors = validation.validateHaiku('newslug', 'string', 1, 5, 100, 20, 1000)

        # Check for error.
        self.assertEqual(errors['word_round_length'], [e['mustBeInt']])


    def testNoSlicingInterval(self):

        '''
        Empty slicing interval.
        '''

        # None slicing interval.
        errors = validation.validateHaiku('newslug', 1000, None, 5, 100, 20, 1000)

        # Check for error.
        self.assertEqual(errors['slicing_interval'], [e['noInterval']])


    def testNonIntSlicingInterval(self):

        '''
        Non-integer slicing interval.
        '''

        # String slicing interval.
        errors = validation.validateHaiku('newslug', 1000, 'string', 5, 100, 20, 1000)

        # Check for error.
        self.assertEqual(errors['slicing_interval'], [e['mustBeInt']])


    def testNoMinBlindSubmissions(self):

        '''
        Empty minimum blind submissions.
        '''

        # None min blind submissions.
        errors = validation.validateHaiku('newslug', 1000, 1, None, 100, 20, 1000)

        # Check for error.
        self.assertEqual(errors['min_blind_submissions'], [e['noMinSubmissions']])


    def testNonIntMinBlindSubmissions(self):

        '''
        Non-integer minimum blind submissions.
        '''

        # String min blind submissions.
        errors = validation.validateHaiku('newslug', 1000, 1, 'string', 100, 20, 1000)

        # Check for error.
        self.assertEqual(errors['min_blind_submissions'], [e['mustBeInt']])


    def testNoBlindSubmissionValue(self):

        '''
        Empty blind submission value.
        '''

        # None blind submission value.
        errors = validation.validateHaiku('newslug', 1000, 1, 5, None, 20, 1000)

        # Check for error.
        self.assertEqual(errors['blind_submission_value'], [e['noSubmissionValue']])


    def testNonIntBlindSubmissionValue(self):

        '''
        Non-integer blind submission value.
        '''

        # String blind submission value.
        errors = validation.validateHaiku('newslug', 1000, 1, 5, 'string', 20, 1000)

        # Check for error.
        self.assertEqual(errors['blind_submission_value'], [e['mustBeInt']])


    def testNoHalfLife(self):

        '''
        Empty half life.
        '''

        # None half life.
        errors = validation.validateHaiku('newslug', 1000, 1, 5, 100, None, 1000)

        # Check for error.
        self.assertEqual(errors['decay_half_life'], [e['noHalfLife']])


    def testNonIntHalfLife(self):

        '''
        Non-integer half life.
        '''

        # String half life.
        errors = validation.validateHaiku('newslug', 1000, 1, 5, 100, 'string', 1000)

        # Check for error.
        self.assertEqual(errors['decay_half_life'], [e['mustBeInt']])


    def testNoSeedCapital(self):

        '''
        Empty seed capital.
        '''

        # None seed capital.
        errors = validation.validateHaiku('newslug', 1000, 1, 5, 100, 20, None)

        # Check for error.
        self.assertEqual(errors['seed_capital'], [e['noCapital']])


    def testNonIntSeedCapital(self):

        '''
        Non-integer seed capital.
        '''

        # String seed capital.
        errors = validation.validateHaiku('newslug', 1000, 1, 5, 100, 20, 'string')

        # Check for error.
        self.assertEqual(errors['seed_capital'], [e['mustBeInt']])



if __name__ == '__main__':
    u.unittest.main()
