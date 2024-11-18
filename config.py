import os

BOARD_SIZE = 5

#à ajuster
EPS = 0.9
GAMMA = 0.5
LEARNING_RATE = 0.5

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')