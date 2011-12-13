'''
Unit tests for the haiku model.
'''

from eh import app, db, sched
from eh.models import Haiku, User
import UnitTestCase as u
import datetime as dt
import math


class UserModelUnitTest(u.UnitTestCase):


    def testRecordInitialization(self):

        '''
        __init__() should create the object and set starting attributes.
        '''

        # Create user and haiku.
        user = User.createAdministrator('username', 'password')
        haiku = Haiku(user.id, 'test', 1000, 1, 5, 100, 30, 1000)

        # Get time delta.
        timeDelta = (dt.datetime.now() - haiku.created_on).total_seconds()

        # Check attribute assignments.
        self.assertEqual(haiku.created_by, user.id)
        self.assertEqual(haiku.url_slug, 'test')
        self.assertEqual(haiku.word_round_length, 1000)
        self.assertEqual(haiku.slicing_interval, 1)
        self.assertEqual(haiku.min_blind_submissions, 5)
        self.assertEqual(haiku.blind_submission_value, 100)
        self.assertEqual(haiku.decay_mean_lifetime, 30 / math.log(2))
        self.assertEqual(haiku.seed_capital, 1000)
        self.assertLess(timeDelta, 0.1)


    def testCreateHaiku(self):

        '''
        createHaiku() should create and save a new record.
        '''

        # At start, no records.
        self.assertEquals(Haiku.query.count(), 0)

        # Create records.
        user = User.createAdministrator('username', 'password')
        haiku = Haiku.createHaiku(user.id, 'test', 1000, 1, 5, 100, 30, 1000)

        # Get time delta.
        timeDelta = (dt.datetime.now() - haiku.created_on).total_seconds()

        # Check for the new record, fetch.
        self.assertEquals(Haiku.query.count(), 1)
        retrievedHaiku = Haiku.query.get(haiku.id)

        # Check attribute assignments.
        self.assertEqual(retrievedHaiku.created_by, user.id)
        self.assertEqual(retrievedHaiku.url_slug, 'test')
        self.assertEqual(retrievedHaiku.word_round_length, 1000)
        self.assertEqual(retrievedHaiku.slicing_interval, 1)
        self.assertEqual(retrievedHaiku.min_blind_submissions, 5)
        self.assertEqual(retrievedHaiku.blind_submission_value, 100)
        self.assertEqual(retrievedHaiku.decay_mean_lifetime, 30 / math.log(2))
        self.assertEqual(retrievedHaiku.seed_capital, 1000)
        self.assertLess(timeDelta, 0.1)


    def testGetHaikuBySlug(self):

        '''
        getHaikuBySlug() should get a record by the url slug.
        '''

        # Create records.
        user = User.createAdministrator('username', 'password')
        haiku = Haiku.createHaiku(user.id, 'test', 1000, 1, 5, 100, 30, 1000)

        # Fetch and check.
        retrievedHaiku = Haiku.getHaikuBySlug('test')
        self.assertEquals(haiku.id, retrievedHaiku.id)


    def testDeleteHaiku(self):

        '''
        deleteHaiku() should delete a record.
        '''

        # Create records.
        user = User.createAdministrator('username', 'password')
        haiku1 = Haiku.createHaiku(user.id, 'test1', 1000, 1, 5, 100, 30, 1000)
        haiku2 = Haiku.createHaiku(user.id, 'test2', 1000, 1, 5, 100, 30, 1000)

        # At start, two records.
        self.assertEquals(Haiku.query.count(), 2)

        # Delete and check.
        Haiku.deleteHaiku(haiku1.id)
        self.assertEquals(Haiku.query.count(), 1)
        retrievedHaiku = Haiku.query.first()
        self.assertEquals(retrievedHaiku.id, haiku2.id)



if __name__ == '__main__':
    u.unittest.main()
