'''
A single word selection episode in a poem.
'''

# Get application assets.
from eh import db
import datetime as dt
import math


class Round(db.Model):

    ''' Word rounds. '''

    # Table name:
    __tablename__ = 'rounds'

    # System attributes:
    id = db.Column(db.Integer, primary_key=True)


    # Row methods:

    def __init__(self):

        ''' Set parameters. '''

        pass


    # Table methods.

    @classmethod
    def createRound(self):

        ''' Create a new round. '''

        # ** set.

        # db.session.add(round)
        # db.session.commit()

        # return round

        pass
