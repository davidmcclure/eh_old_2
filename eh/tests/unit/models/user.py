'''
Unit tests for the user model.
'''

from eh import app, db
import unittest
from werkzeug.security import check_password_hash
from eh.models import User


class UserModelUnitTest(unittest.TestCase):


    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memory'
        app.config['TESTING'] = True
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def testRecordInitialization(self):

        ''' Test object creation and starting attribute setting. '''

        user = User('username', 'password', True)

        # Check attribute assignments.
        self.assertEqual(user.username, 'username')
        self.assertEqual(user.is_admin, True)
        self.assertIsNotNone(user.password_hash)


    def testSetPassword(self):

        ''' Test password hashing. '''

        user = User('username', 'password', True)

        # Check the hash comparer.
        correct = check_password_hash(user.password_hash, 'password')
        self.assertEqual(correct, True)
        incorrect = check_password_hash(user.password_hash, 'wrong')
        self.assertEqual(incorrect, False)


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


if __name__ == '__main__':
    unittest.main()
