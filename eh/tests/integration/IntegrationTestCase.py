'''
Abstract class for integration tests.
'''

from eh import app, db
import unittest
import blinker
from flask import template_rendered


class IntegrationTestCase(unittest.TestCase):


    def setUp(self):

        '''
        Create database, set testing mode, create testing client, get
        template tracking set up.
        '''

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

        self.templates = []
        template_rendered.connect(self.addTemplate)


    def addTemplate(self,app, template, context):

        '''
        Register templates.
        '''

        self.templates.append((template, context))


    def tearDown(self):

        '''
        Kill the database session, drop the tables.
        '''

        db.session.remove()
        db.drop_all()


    def assertTemplateUsed(self, name):

        '''
        Checks to see if template is rendered.
        '''

        for template, context in self.templates:
            if template.name == name:
                return True

        raise AssertionError, "template %s not used" % name


    def assertRedirect(self, response, location):

        '''
        Check for redirect.
        '''

        self.assertIn(response.status_code, (301, 302))
        self.assertLocation(response, location)


    def assertLocation(self, response, location):

        '''
        Check for for a location.
        '''

        self.assertEquals(response.location, 'http://localhost' + location)



if __name__ == '__main__':
    unittest.main()
