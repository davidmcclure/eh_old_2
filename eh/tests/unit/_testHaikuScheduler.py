'''
Unit tests for the user model.
'''

from eh import app, db
from eh.models import User, Haiku
from eh.helpers.scheduler import HaikuScheduler
import UnitTestCase as u


class HaikuSchedulerUnitTest(u.UnitTestCase):


    def setUp(self):

        ''' Instantiate the scheduler. '''

        super(HaikuSchedulerUnitTest, self).setUp()

        # Create admin and haiku.
        self.user = User.createAdministrator('username', 'password')
        self.haiku = Haiku.createHaiku(self.user.id, 'test', 1000, 1, 5, 100, 30, 1000)

        # Instantiate the scheduler.
        self.sched = HaikuScheduler()
        self.sched.start()


    def testGetJobName(self):

        '''
        Test job name construction.
        '''

        # Get job name.
        name = self.sched.getJobName(self.haiku)

        # Check name construction.
        self.assertEquals(name, 'username' + str(self.haiku.id))


    def testGetJobByHaikuWhenJobDoesNotExist(self):

        '''
        getJobByHaiku() should return False when there is no job.
        '''

        # Should return False for no job.
        self.assertFalse(self.sched.getJobByHaiku(self.haiku))


    def testGetJobByHaikuWhenJobExists(self):

        '''
        getJobByHaiku() should return the job when it exists.
        '''

        # Dummy slicing routine.
        def testSlicer():
            pass

        # Add a slicer.
        job = self.sched.add_interval_job(
            func = testSlicer,
            name = self.sched.getJobName(self.haiku),
            seconds = 1,
            jobstore = HaikuScheduler.JOBSTORE)

        # Should return the job.
        self.assertEquals(job, self.sched.getJobByHaiku(self.haiku))


    def testCheckForSlicerWhenFalse(self):

        '''
        checkForSlicer() should return False when there is not a slicer.
        '''

        # Should be no slicer by default.
        self.assertFalse(self.sched.checkForSlicer(self.haiku))


    def testCheckForSlicerWhenTrue(self):

        '''
        checkForSlicer() should return True when there is a slicer.
        '''

        # Dummy slicing routine.
        def testSlicer():
            pass

        # Add a slicer.
        self.sched.add_interval_job(
            func = testSlicer,
            name = self.sched.getJobName(self.haiku),
            seconds = 1,
            jobstore = HaikuScheduler.JOBSTORE)

        # Should detect the slicer.
        self.assertTrue(self.sched.checkForSlicer(self.haiku))


    def testCreateSlicer(self):

        '''
        createSlicer() should add a new slicer for the haiku.
        '''

        # Dummy slicing routine.
        def testSlicer():
            pass

        # Add a slicer.
        slicer = self.sched.createSlicer(self.haiku, testSlicer, 1)

        # Check the attributes.
        self.assertEquals(slicer.name, 'username' + str(self.haiku.id))
        self.assertEquals(slicer.func, testSlicer)

        # Confirm that the job is stored in the scheduler.
        self.assertIn(slicer, self.sched.get_jobs())


    def testCreateSlicerNoDuplicates(self):

        '''
        createSlicer() should not create a slicer if one already exists for the
        passed haiku record.
        '''

        # Dummy slicing routine.
        def testSlicer():
            pass

        # Add a slicer.
        self.sched.add_interval_job(
            func = testSlicer,
            name = self.sched.getJobName(self.haiku),
            seconds = 1,
            jobstore = HaikuScheduler.JOBSTORE)

        # Tru to add a slicer.
        slicer = self.sched.createSlicer(self.haiku, testSlicer, 1)
        self.assertFalse(slicer)

        # Confirm that the job is not stored in the scheduler.
        self.assertNotIn(slicer, self.sched.get_jobs())


    def testDeleteSlicer(self):

        '''
        deleteSlicer() should delete the correct slicer.
        '''

        # Create a second haiku.
        haiku2 = Haiku.createHaiku(self.user.id, 'test2', 1000, 1, 5, 100, 30, 1000)

        # Dummy slicing routine.
        def testSlicer():
            pass

        # Add two slicers.
        self.sched.add_interval_job(
            func = testSlicer,
            name = self.sched.getJobName(self.haiku),
            seconds = 1,
            jobstore = HaikuScheduler.JOBSTORE)

        self.sched.add_interval_job(
            func = testSlicer,
            name = self.sched.getJobName(haiku2),
            seconds = 1,
            jobstore = HaikuScheduler.JOBSTORE)

        # Should be 2 jobs.
        self.assertEquals(len(self.sched.get_jobs()), 2)

        # Delete the second slicer.
        self.sched.deleteSlicer(haiku2)

        # Should be 1 job.
        self.assertEquals(len(self.sched.get_jobs()), 1)

        # Check that the right slicer was deleted.
        self.assertTrue(self.sched.checkForSlicer(self.haiku))
        self.assertFalse(self.sched.checkForSlicer(haiku2))



if __name__ == '__main__':
    u.unittest.main()
