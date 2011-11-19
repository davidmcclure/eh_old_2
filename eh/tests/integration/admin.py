'''
Unit tests for the user model.
'''

from eh import app, db
import unittest


class AdminControllerTest(unittest.TestCase):


    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memory'
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def testBrowseRedirectWhenNoAdmin(self):

        ''' If there is not an admin in the database, the browse view should
        redirect to the first-admin registraton view. '''

        rv = self.app.get('/admin')



if __name__ == '__main__':
    unittest.main()
