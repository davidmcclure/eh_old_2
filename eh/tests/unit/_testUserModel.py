'''
Unit tests for the user model.
'''

from eh import app, db
from werkzeug.security import check_password_hash
from eh.models import User
import UnitTestCase as u


class UserModelUnitTest(u.UnitTestCase):


    def testRecordInitialization(self):

        '''
        Test object creation and starting attribute setting.
        '''

        user = User('username', 'password', True)

        # Check attribute assignments.
        self.assertEqual(user.username, 'username')
        self.assertTrue(user.is_admin)
        self.assertIsNotNone(user.password_hash)


    def testSetPassword(self):

        '''
        Test password hashing.
        '''

        user = User('username', 'password', True)

        # Check the hash comparer.
        correct = check_password_hash(user.password_hash, 'password')
        self.assertTrue(correct)
        incorrect = check_password_hash(user.password_hash, 'wrong')
        self.assertFalse(incorrect)


    def testCheckPassword(self):

        '''
        Test password checking.
        '''

        user = User('username', 'password', True)
        self.assertTrue(user.checkPassword('password'))
        self.assertFalse(user.checkPassword('wrong'))


    def testUserExists(self):

        '''
        userExists() should check if there is at least one admin.
        '''

        # False with no administrators.
        self.assertFalse(User.userExists())

        admin = User('username', 'password', True)
        db.session.add(admin)
        db.session.commit()

        # True with an administrator.
        self.assertTrue(User.userExists())


    def testUserIsAdmin(self):

        '''
        userIsAdmin() should check if user with a given id is an admin.
        '''

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


    def testGetUserByName(self):

        '''
        getUserByName() should retrieve a user with a given name and return
        False if there is no user with the name.
        '''

        # False with no user.
        self.assertFalse(User.getUserByName('user'))

        user = User('user', 'password', False)
        db.session.add(user)
        db.session.commit()

        # When user exists, returns record.
        userRecord = User.getUserByName('user')
        self.assertEquals(user.id, userRecord.id)


    def testCreateAdministrator(self):

        '''
        createAdministrator() should create a new administrator.
        '''

        # At start, no users.
        self.assertEquals(User.query.count(), 0)

        # Create the administrator.
        user = User.createAdministrator('username', 'password')

        # 1 user.
        self.assertEquals(User.query.count(), 1)

        # Check attributes.
        self.assertEquals(user.username, 'username')
        self.assertTrue(check_password_hash(user.password_hash, 'password'))
        self.assertTrue(user.is_admin)


    def testCreateUser(self):

        '''
        createUser() should create a new non-admin user.
        '''

        # At start, no users.
        self.assertEquals(User.query.count(), 0)

        # Create the administrator.
        user = User.createUser('username', 'password')

        # 1 user.
        self.assertEquals(User.query.count(), 1)

        # Check attributes.
        self.assertEquals(user.username, 'username')
        self.assertTrue(check_password_hash(user.password_hash, 'password'))
        self.assertFalse(user.is_admin)


if __name__ == '__main__':
    u.unittest.main()
