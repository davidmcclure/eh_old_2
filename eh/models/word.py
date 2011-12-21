'''
A candidate word for a given haiku and selection round.
'''

# Get application assets.
from eh import db
import datetime as dt
import math


class Word(db.Model):

    ''' Word submissions. '''

    # Table name:
    __tablename__ = 'words'

    # System attributes:
    id = db.Column(db.Integer, primary_key=True)


    # Row methods:

    def __init__(self):

        ''' Set parameters. '''

        pass


    # Table methods.

    @classmethod
    def createWord(self):

        ''' Create a new word. '''

        # ** set.

        # db.session.add(round)
        # db.session.commit()

        # return round

        pass
