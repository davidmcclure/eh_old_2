'''
Integration tests for the admin controller.
'''

# Get the abstract class and models.
import IntegrationTestCase as i
from eh import sched
from eh.models import User, Haiku
from eh.helpers import slicer
from eh.lib.messages import errors as e
from werkzeug.security import check_password_hash
from flask import session
import math


class AdminBrowseTest(i.IntegrationTestCase):

    ''' /admin '''


    pass



class AdminNewTest(i.IntegrationTestCase):

    ''' /admin/new '''


    def testForm(self):

        '''
        With a GET request, /admin/new should show the form.
        '''

        # Create an admin.
        admin = User.createAdministrator('username', 'password')

        with self.app as c:

            # Push in a user id.
            with c.session_transaction() as s:
                s['user_id'] = admin.id

            # Hit the route.
            rv = c.get('/admin/new')
            self.assertTemplateUsed('admin/new.html')


    def testFailure(self):

        '''
        Flash errors for invalid submission.
        '''

        # Create an admin.
        admin = User.createAdministrator('username', 'password')

        with self.app as c:

            # Push in a user id.
            with c.session_transaction() as s:
                s['user_id'] = admin.id

            # At start, no haiku.
            self.assertEquals(Haiku.query.count(), 0)

            # Empty fields
            rv = c.post('/admin/new', data=dict(
                url_slug = '',
                word_round_length = '',
                slicing_interval = '',
                min_blind_submissions = '',
                blind_submission_value = '',
                decay_half_life = '',
                seed_capital = ''
            ), follow_redirects=True)

            # Should re-render register template.
            self.assertTemplateUsed('admin/new.html')

            # Check for errors.
            assert e['noSlug'] in rv.data
            assert e['noRoundLength'] in rv.data
            assert e['noInterval'] in rv.data
            assert e['noMinSubmissions'] in rv.data
            assert e['noSubmissionValue'] in rv.data
            assert e['noHalfLife'] in rv.data
            assert e['noCapital'] in rv.data

            # No user should have been created.
            self.assertEquals(Haiku.query.count(), 0)


    def testSuccess(self):

        '''
        Valid form should create new haiku.
        '''

        # Create an admin.
        admin = User.createAdministrator('username', 'password')

        with self.app as c:

            # Push in a user id.
            with c.session_transaction() as s:
                s['user_id'] = admin.id

            # At start, no haiku.
            self.assertEquals(Haiku.query.count(), 0)

            # Empty fields
            rv = c.post('/admin/new', data=dict(
                url_slug = 'test',
                word_round_length = 1000,
                slicing_interval = 1,
                min_blind_submissions = 5,
                blind_submission_value = 100,
                decay_half_life = 30,
                seed_capital = 1000
            ), follow_redirects=True)

            # Should re-render register template.
            self.assertTemplateUsed('admin/browse.html')

            # No user should have been created.
            self.assertEquals(Haiku.query.count(), 1)

            # Get the haiku and test the attributes.
            haiku = Haiku.query.first()
            self.assertEquals(haiku.url_slug, 'test')
            self.assertEquals(haiku.word_round_length, 1000)
            self.assertEquals(haiku.slicing_interval, 1)
            self.assertEquals(haiku.min_blind_submissions, 5)
            self.assertEquals(haiku.blind_submission_value, 100)
            self.assertEquals(haiku.decay_mean_lifetime, 30 / math.log(2))
            self.assertEquals(haiku.seed_capital, 1000)



class AdminDeleteTest(i.IntegrationTestCase):

    ''' /admin/delete '''


    def testDelete(self):

        '''
        A GET request should delete the haiku.
        '''

        # Create an admin and haiku.
        admin = User.createAdministrator('username', 'password')

        # Create 2 haiku.
        haiku1 = Haiku.createHaiku(admin.id, 'test1', 1000, 1, 5, 100, 30, 1000)
        haiku2 = Haiku.createHaiku(admin.id, 'test2', 1000, 1, 5, 100, 30, 1000)

        with self.app as c:

            # Re-get the haiku.
            haiku1 = Haiku.getHaikuBySlug('test1')
            haiku2 = Haiku.getHaikuBySlug('test2')

            # Push in a user id.
            with c.session_transaction() as s:
                s['user_id'] = admin.id

            # At the start, 2 records.
            self.assertEquals(Haiku.query.count(), 2)

            # Hit the route.
            rv = c.get('/admin/delete/' + str(haiku1.id), follow_redirects=True)
            self.assertTemplateUsed('admin/browse.html')

            # 1 record.
            self.assertEquals(Haiku.query.count(), 1)

            # Check that the right record was deleted.
            haiku = Haiku.query.first()
            self.assertEquals(haiku.id, haiku2.id)



class AdminStartTest(i.IntegrationTestCase):

    ''' /admin/start '''


    def testStart(self):

        '''
        A GET request should run the slicer for the haiku.
        '''

        # Create an admin and haiku.
        admin = User.createAdministrator('username', 'password')
        haiku = Haiku.createHaiku(admin.id, 'test', 1000, 1, 5, 100, 30, 1000)

        with self.app as c:

            # Re-get the haiku.
            haiku = Haiku.getHaikuBySlug('test')

            # Push in a user id.
            with c.session_transaction() as s:
                s['user_id'] = admin.id

            # Hit the route, check for redirect back to browse.
            rv = c.get('/admin/start/' + str(haiku.id), follow_redirects=True)
            self.assertTemplateUsed('admin/browse.html')

            # Check for the slicer.
            job = sched.getJobByHaiku(haiku)
            self.assertIsNot(job, False)



class AdminStopTest(i.IntegrationTestCase):

    ''' /admin/stop '''


    def testStop(self):

        '''
        A GET request should stop the slicer for a haiku.
        '''

        # Create an admin and haiku.
        admin = User.createAdministrator('username', 'password')
        haiku = Haiku.createHaiku(admin.id, 'test', 1000, 1, 5, 100, 30, 1000)

        # Start the slicer
        sched.createSlicer(haiku, slicer.slice)

        with self.app as c:

            # Re-get the haiku.
            haiku = Haiku.getHaikuBySlug('test')

            # Push in a user id.
            with c.session_transaction() as s:
                s['user_id'] = admin.id

            # Hit the route, check for redirect back to browse.
            rv = c.get('/admin/stop/' + str(haiku.id), follow_redirects=True)
            self.assertTemplateUsed('admin/browse.html')

            # Check that the slicer is not present.
            job = sched.getJobByHaiku(haiku)
            self.assertFalse(job)



class AdminRegisterTest(i.IntegrationTestCase):

    ''' /admin/register '''


    def testForm(self):

        '''
        With a GET request, /admin/register should show the form.
        '''

        # Hit with GET.
        rv = self.app.get('/admin/register')
        self.assertTemplateUsed('admin/register.html')


    def testFailure(self):

        '''
        Flash errors for invalid submission.
        '''

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


    def testSuccess(self):

        '''
        Valid registration form should create user.
        '''

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


    def testForm(self):

        '''
        With a GET request, /admin/login should show the form.
        '''

        # Create an admin.
        admin = User.createAdministrator('username', 'password')

        # Hit with GET.
        rv = self.app.get('/admin/login')
        self.assertTemplateUsed('admin/login.html')


    def testFailure(self):

        '''
        Flash errors when fields are empty.
        '''

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


    def testSuccess(self):

        '''
        Valid credentials should log the admin in.
        '''

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

        '''
        Existing user_id should be popped off of session.
        '''

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

        '''
        Logout route should redirect to login.
        '''

        # Create admin.
        admin = User.createAdministrator('username', 'password')

        # With no user_id in the session hash.
        rv = self.app.get('/admin/logout')
        self.assertRedirect(rv, '/admin/login')


if __name__ == '__main__':
    i.unittest.main()
