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
    haiku_id = db.Column(db.Integer, db.ForeignKey('haiku.id'))
    round_id = db.Column(db.Integer, db.ForeignKey('rounds.id'))
    word = db.Column(db.String(60))


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
