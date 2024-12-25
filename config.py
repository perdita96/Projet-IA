import os

BOARD_SIZE = 5

#à ajuster
EPS = 0.13397967485796175
MIN_EPSILON = 0.1
DISCOUNT_FACTOR  = 0.9
LEARNING_RATE = 0.3
MAX_GAMES = 200000
DECAY_RATE = 0.99
EPSILON_UPDATE_PARTIE = 500

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')