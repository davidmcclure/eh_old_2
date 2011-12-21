'''
An allocation of points to a word in a given haiku and round.
'''

# Get application assets.
from eh import db
import datetime as dt
import math


class Allocation(db.Model):

    ''' Point allocations to words. '''

    # Table name:
    __tablename__ = 'allocations'

    # System attributes:
    id = db.Column(db.Integer, primary_key=True)


    # Row methods:

    def __init__(self):

        ''' Set parameters. '''

        pass


    # Table methods.

    @classmethod
    def createAllocation(self):

        ''' Apply an allocation. '''

        # ** set.

        # db.session.add(round)
        # db.session.commit()

        # return round

        pass
