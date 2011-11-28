'''
Unit tests for the user model.
'''

# Get the abstract class and models.
import IntegrationTestCase as i
from eh.models import User
from werkzeug.security import check_password_hash
from flask import session


class AdminBrowseTest(i.IntegrationTestCase):

    ''' /admin '''


    def testRedirectWhenNoAdmin(self):

        ''' If there is not an admin in the database, the browse view should
        redirect to the first-admin registraton view. '''

        rv = self.app.get('/admin')
        self.assertRedirect(rv, '/admin/register')


    def testRedirectWhenAdminNotLoggedIn(self):

        ''' If there is an admin, but the user is not logged in as an admin,
        redirect to login. '''

        # Create admin.
        User.createAdministrator('username', 'password')

        rv = self.app.get('/admin')
        self.assertRedirect(rv, '/admin/login')


class AdminRegisterTest(i.IntegrationTestCase):

    ''' /admin/register '''


    def testRedirectWhenAdmin(self):

        ''' If there is an admin in the database, the register view should
        redirect to the login view. '''

        # Create admin.
        User.createAdministrator('username', 'password')

        rv = self.app.get('/admin/register')
        self.assertRedirect(rv, '/admin/login')


    def testNoRedirectWhenNoAdmin(self):

        ''' If no admin in the database, do not redirect. '''

        # Should render register template.
        rv = self.app.get('/admin/register')
        self.assertEquals(rv.status_code, 200)
        self.assertTemplateUsed('admin/register.html')


    def testErrorFlashing(self):

        ''' Validation errors should be displayed for invalid form submissions. '''

        # Empty fields
        rv = self.app.post('/admin/register', data=dict(
            username = '',
            password = '',
            confirm = '',
        ), follow_redirects=True)

        # Should re-render register template.
        self.assertTemplateUsed('admin/register.html')

        # Check for errors.
        assert 'Enter a username.' in rv.data
        assert 'Enter a password.' in rv.data
        assert 'Confirm your password.' in rv.data

        # Mismatched password and confirmation.
        rv = self.app.post('/admin/register', data=dict(
            username = 'username',
            password = 'password',
            confirm = 'nomatch',
        ), follow_redirects=True)

        # Should re-render register template.
        self.assertTemplateUsed('admin/register.html')

        # Check for errors.
        assert 'Does not match.' in rv.data


    def testAdminCreation(self):

        ''' Valid inputs should create a new administrator and redirect to the
        browse view. '''

        # At start, no users.
        self.assertEquals(User.query.count(), 0)

        # Empty fields
        rv = self.app.post('/admin/register', data=dict(
            username = 'username',
            password = 'password',
            confirm = 'password',
        ), follow_redirects=True)

        # Should re-render register template.
        self.assertTemplateUsed('admin/browse.html')

        # 1 user.
        self.assertEquals(User.query.count(), 1)

        # Get the user and test attributes.
        user = User.query.first()
        self.assertEquals(user.username, 'username')
        self.assertTrue(check_password_hash(user.password_hash, 'password'))


class AdminLogoutTest(i.IntegrationTestCase):

    ''' /admin/logout '''


    def testUserIdKeyPop(self):

        ''' The logout route should pop the user_id key off of the session
        hash, if there is one. '''

        with self.app as c:

            # Push in a user id.
            with c.session_transaction() as s:
                s['user_id'] = 1

            # Check for the presence of the id.
            self.assertEquals(session['user_id'], 1)

            # Hit the logout route, confirm that the id is gone.
            rv = c.get('admin/logout')
            self.assertNotIn(session, 'user_id')


    def testRedirect(self):

        ''' The logout route should redirect to login. '''

        # With no user_id in the session hash.
        rv = self.app.get('admin/logout')
        self.assertRedirect(rv, '/admin/login')


if __name__ == '__main__':
    i.unittest.main()
