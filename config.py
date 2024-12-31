import os

BOARD_SIZE = 5

#à ajuster
EPS = 0.1
MIN_EPSILON = 0.1
DISCOUNT_FACTOR  = 0.9
LEARNING_RATE = 0.3
MAX_GAMES = 200000
DECAY_RATE = 0.99
EPSILON_UPDATE_PARTIE = 500


#configuration de l'application Flask
basedir = os.path.abspath(os.path.dirname(__file__))
#défini URI de connection
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')