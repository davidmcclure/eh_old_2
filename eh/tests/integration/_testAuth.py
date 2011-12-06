'''
Tests for authorization decorators.
'''

# Get the abstract class and models.
import IntegrationTestCase as i
from eh.models import User
from eh.helpers import auth
from eh import app, db
from flask import session


class AuthTest(i.IntegrationTestCase):


    def testIsAdminWithNoUser(self):

        '''
        If there is no user in the session, isAdmin() should redirect to /login.
        '''

        # Test method.
        @app.route('/test')
        @auth.isAdmin
        def test(admin):
            return 'executed'

        # With no user_id in the session, redirect to login.
        rv = self.app.get('/test')
        self.assertRedirect(rv, '/admin/login')


    def testIsAdminWithNonAdminUser(self):

        '''
        If there is a non-admin user in the session, redirect to /login.
        '''

        # Test method.
        @app.route('/test')
        @auth.isAdmin
        def test(admin):
            return 'executed'

        # With non-admin user_id in session, redirect to login.
        with self.app as c:

            user = User.createUser('username', 'password')

            # Push in a user id.
            with c.session_transaction() as s:
                s['user_id'] = user.id

            rv = c.get('/test')
            self.assertRedirect(rv, '/admin/login')


    def testIsAdminWithAdminUser(self):

        '''
        If there is an admin in the session, execute the method.
        '''

        # Test method.
        @app.route('/test')
        @auth.isAdmin
        def test(admin):
            return 'executed'

        # With admin user_id in session, execute.
        with self.app as c:

            admin = User.createAdministrator('username', 'password')

            # Push in a user id.
            with c.session_transaction() as s:
                s['user_id'] = admin.id

            rv = c.get('/test')
            self.assertEquals(rv.status_code, 200)
            assert 'executed' in rv.data



if __name__ == '__main__':
    i.unittest.main()
