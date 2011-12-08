'''
Unit tests for the user model.
'''

# Get the abstract class and models.
import IntegrationTestCase as i
from eh.models import User
from eh.lib.messages import errors as e
from werkzeug.security import check_password_hash
from flask import session


class AdminBrowseTest(i.IntegrationTestCase):

    ''' /admin '''


    def testHaikuListing(self):

        ''' The browse view should display the haiku. '''

        pass



class AdminRegisterTest(i.IntegrationTestCase):

    ''' /admin/register '''


    def testEmptyFields(self):

        ''' Flash errors for empty fields. '''

        # At start, no users.
        self.assertEquals(User.query.count(), 0)

        # Empty fields
        rv = self.app.post('/admin/register', data=dict(
            username = '',
            password = '',
            confirm = '',
        ), follow_redirects=True)

        # Should re-render register template.
        self.assertTemplateUsed('admin/register.html')

        # Check for errors.
        assert e['noUsername'] in rv.data
        assert e['noPassword'] in rv.data
        assert e['noConfirm'] in rv.data

        # No user should have been created.
        self.assertEquals(User.query.count(), 0)


    def testPasswordConfirmationMismatch(self):

        ''' Flash errors for not-matching password confirm. '''

        # At start, no users.
        self.assertEquals(User.query.count(), 0)

        # Empty fields
        rv = self.app.post('/admin/register', data=dict(
            username = 'username',
            password = 'password',
            confirm = 'nomatch',
        ), follow_redirects=True)

        # Should re-render register template.
        self.assertTemplateUsed('admin/register.html')

        # Check for errors.
        assert e['confirmDoesNotMatch'] in rv.data

        # No user should have been created.
        self.assertEquals(User.query.count(), 0)


    def testAdminCreation(self):

        ''' Valid registration form should create user. '''

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



class AdminLoginTest(i.IntegrationTestCase):

    ''' /admin/login '''


    def testEmptyFields(self):

        ''' Flash errors when fields are empty. '''

        # Create an admin.
        admin = User.createAdministrator('username', 'password')

        with self.app as c:

            # Empty fields
            rv = c.post('/admin/login', data=dict(
                username = '',
                password = ''
            ), follow_redirects=True)

            # Should re-render login template.
            self.assertTemplateUsed('admin/login.html')

            # Check for errors.
            assert e['noUsername'] in rv.data
            assert e['noPassword'] in rv.data

            # Confirm that there is no id.
            with c.session_transaction() as s:
                self.assertNotIn('user_id', s)


    def testEmptyFields(self):

        ''' Flash errors with non-existent username. '''

        # Create an admin.
        admin = User.createAdministrator('username', 'password')

        with self.app as c:

            # Empty fields
            rv = c.post('/admin/login', data=dict(
                username = 'doesnotexist',
                password = 'password'
            ), follow_redirects=True)

            # Should re-render login template.
            self.assertTemplateUsed('admin/login.html')

            # Check for errors.
            assert e['usernameDoesNotExist'] in rv.data

            # Confirm that there is no id.
            with c.session_transaction() as s:
                self.assertNotIn('user_id', s)


    def testWrongPassword(self):

        ''' Flash errors with incorrect password. '''

        # Create an admin.
        admin = User.createAdministrator('username', 'password')

        with self.app as c:

            # Empty fields
            rv = c.post('/admin/login', data=dict(
                username = 'username',
                password = 'wrong'
            ), follow_redirects=True)

            # Should re-render login template.
            self.assertTemplateUsed('admin/login.html')

            # Check for errors.
            assert e['incorrectPassword'] in rv.data

            # Confirm that there is no id.
            with c.session_transaction() as s:
                self.assertNotIn('user_id', s)


    def testNotAuthorized(self):

        ''' Flash errors with non-admin credentials. '''

        # Create an admin.
        admin = User.createUser('username', 'password')

        with self.app as c:

            # Empty fields
            rv = c.post('/admin/login', data=dict(
                username = 'username',
                password = 'password'
            ), follow_redirects=True)

            # Should re-render login template.
            self.assertTemplateUsed('admin/login.html')

            # Check for errors.
            assert e['notAuthorized'] in rv.data

            # Confirm that there is no id.
            with c.session_transaction() as s:
                self.assertNotIn('user_id', s)


    def testLoginSuccess(self):

        ''' Valid credentials should log the admin in. '''

        # Create an admin.
        admin = User.createAdministrator('username', 'password')

        with self.app as c:

            # Empty fields
            rv = c.post('/admin/login', data=dict(
                username = 'username',
                password = 'password'
            ), follow_redirects=True)

            # Should re-render login template.
            self.assertTemplateUsed('admin/browse.html')

            # Confirm that there is no id.
            with c.session_transaction() as s:
                self.assertEquals(s['user_id'], admin.id)



class AdminLogoutTest(i.IntegrationTestCase):

    ''' /admin/logout '''


    def testUserIdKeyPop(self):

        ''' Existing user_id should be popped off of session. '''

        # Create admin.
        admin = User.createAdministrator('username', 'password')

        with self.app as c:

            # Push in a user id.
            with c.session_transaction() as s:
                s['user_id'] = admin.id

            # Check for the presence of the id.
            self.assertEquals(s['user_id'], 1)

            # Hit the logout route.
            rv = c.get('/admin/logout')

            # Confirm that the id is gone.
            with c.session_transaction() as s:
                self.assertNotIn('user_id', s)


    def testRedirect(self):

        ''' Logout route should redirect to login. '''

        # Create admin.
        admin = User.createAdministrator('username', 'password')

        # With no user_id in the session hash.
        rv = self.app.get('/admin/logout')
        self.assertRedirect(rv, '/admin/login')


if __name__ == '__main__':
    i.unittest.main()
