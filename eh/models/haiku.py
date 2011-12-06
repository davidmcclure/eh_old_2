'''
The core poem model.
'''

# Get application assets.
from eh import app, db
import datetime as dt
import math


class Haiku(db.Model):

    ''' Poems. '''

    # Table name:
    __tablename__ = 'haiku'

    # System attributes:
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_on = db.Column(db.DateTime)
    url_slug = db.Column(db.String(40), unique=True)
    started = db.Column(db.Boolean, default=False)
    finished = db.Column(db.Boolean, default=False)
    is_running = db.Column(db.Boolean, default=False)

    # Rule parameters:
    word_round_length = db.Column(db.Integer)
    slicing_interval = db.Column(db.Integer)
    min_blind_submissions = db.Column(db.Integer)
    blind_submission_value = db.Column(db.Integer)
    decay_mean_lifetime = db.Column(db.Float)
    seed_capital = db.Column(db.Integer)


    # Row methods:

    def __init__(self,
            userId,
            title,
            slug,
            roundLength,
            interval,
            minSubmissions,
            submissionValue,
            halfLife,
            capital):

        ''' Set parameters. '''

        self.created_by =               userId
        self.title =                    title
        self.url_slug =                 slug
        self.created_on =               dt.datetime.now()
        self.word_round_length =        roundLength
        self.slicing_interval =         interval
        self.min_blind_submissions =    minSubmissions
        self.blind_submission_value =   submissionValue
        self.decay_mean_lifetime =      int(halfLife) / math.log(2)
        self.seed_capital =             capital


    # Table methods.

    @classmethod
    def createHaiku(self,
            userId,
            title,
            slug,
            roundLength,
            interval,
            minSubmissions,
            submissionValue,
            halfLife,
            capital):

        ''' Create a new haiku. '''

        haiku = Haiku(
                userId,
                title,
                slug,
                roundLength,
                interval,
                minSubmissions,
                submissionValue,
                halfLife,
                capital)

        db.session.add(haiku)
        db.session.commit()

        return haiku


    @classmethod
    def getHaikuBySlug(self, slug):

        ''' Get haiku with a given slug. '''

        haiku = Haiku.query.filter_by(url_slug=slug).first()
        return haiku if haiku != None else False
