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

        self.assertEqual(user.username, 'username')
        self.assertEqual(user.is_admin, True)
        self.assertIsNotNone(user.password_hash)


    def testSetPassword(self):

        ''' Test password hashing. '''

        user = User('username', 'password', True)

        check = check_password_hash(user.password_hash, 'password')
        self.assertEqual(check, True)


if __name__ == '__main__':
    unittest.main()
