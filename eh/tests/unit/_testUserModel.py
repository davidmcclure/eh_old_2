'''
Unit tests for the user model.
'''

from eh import app, db
from werkzeug.security import check_password_hash
from eh.models import User
import UnitTestCase as u


class UserModelUnitTest(u.UnitTestCase):


    def testRecordInitialization(self):

        ''' Test object creation and starting attribute setting. '''

        user = User('username', 'password', True)

        # Check attribute assignments.
        self.assertEqual(user.username, 'username')
        self.assertTrue(user.is_admin)
        self.assertIsNotNone(user.password_hash)


    def testSetPassword(self):

        ''' Test password hashing. '''

        user = User('username', 'password', True)

        # Check the hash comparer.
        correct = check_password_hash(user.password_hash, 'password')
        self.assertTrue(correct)
        incorrect = check_password_hash(user.password_hash, 'wrong')
        self.assertFalse(incorrect)


    def testAdministratorExists(self):

        ''' Test method that checks if there is at least one admin. '''

        # False with no administrators.
        self.assertFalse(User.administratorExists())

        admin = User('username', 'password', True)
        db.session.add(admin)
        db.session.commit()

        # True with an administrator.
        self.assertTrue(User.administratorExists())


    def testUserIsAdmin(self):

        ''' Test method that checks if user with a given id is an admin. '''

        admin = User('admin', 'password', True)
        user = User('user', 'password', False)
        db.session.add(admin)
        db.session.add(user)
        db.session.commit()

        # True with an administrator, false with user.
        self.assertTrue(User.userIsAdmin(admin.id))
        self.assertFalse(User.userIsAdmin(user.id))

        # False if an id is passed for which there is no record.
        self.assertFalse(User.userIsAdmin(3))


    def testUserNameAvailable(self):

        ''' Test method that checks to see if a username is available. '''

        # True with no user.
        self.assertTrue(User.userNameAvailable('user'))

        user = User('user', 'password', False)
        db.session.add(user)
        db.session.add(user)
        db.session.commit()

        # False with user.
        self.assertFalse(User.userNameAvailable('user'))


    def testCreateAdministrator(self):

        ''' Test method that creates a new administrator. '''

        # At start, no users.
        self.assertEquals(User.query.count(), 0)

        # Create the administrator.
        user = User.createAdministrator('username', 'password')

        # 1 user.
        self.assertEquals(User.query.count(), 1)

        # Check attributes.
        self.assertEquals(user.username, 'username')
        self.assertTrue(check_password_hash(user.password_hash, 'password'))


if __name__ == '__main__':
    u.unittest.main()
