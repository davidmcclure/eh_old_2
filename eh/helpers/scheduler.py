'''
Extension of the APScheduler Scheduler class that manages the slicing jobs.
'''

import eh.models as models
from apscheduler.scheduler import Scheduler
from apscheduler.jobstores.ram_store import RAMJobStore


class HaikuScheduler(Scheduler):

    ''' Manage the slicing jobs. '''


    JOBSTORE = 'eh'


    def __init__(self):

        ''' Add the jobstore. '''

        super(HaikuScheduler, self).__init__()
        self.add_jobstore(RAMJobStore(), HaikuScheduler.JOBSTORE)


    def getJobName(self, haiku):

        ''' Construct the job name for a haiku record. '''

        # Get the record for the admin who created the haiku.
        admin = models.User.query.get(haiku.created_by)

        return admin.username + str(haiku.id)


    def getJobByHaiku(self, haiku):

        ''' Try to retrieve a job for a given haiku record. '''

        name = self.getJobName(haiku)

        for job in self.get_jobs():
            if job.name == name: return job

        return False


    def checkForSlicer(self, haiku):

        ''' Check to see if there is a running slicer for a given haiku. '''

        return True if self.getJobByHaiku(haiku) else False


    def createSlicer(self, haiku, func):

        ''' Start slicing for a poem. '''

        # If a slicer does not already exist, create one.
        if not self.checkForSlicer(haiku):

            return self.add_interval_job(
                func = func,
                seconds = haiku.slicing_interval,
                name = self.getJobName(haiku),
                jobstore = HaikuScheduler.JOBSTORE)

        else: return False


    def deleteSlicer(self, haiku):

        ''' Stop slicing for a poem. '''

        # Get the job.
        slicer = self.getJobByHaiku(haiku)

        # Remove.
        if slicer:
            self.unschedule_job(slicer)
