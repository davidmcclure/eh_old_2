'''
Abstract class for unit tests.
'''

from eh import app, db
import unittest


class UnitTestCase(unittest.TestCase):


    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
