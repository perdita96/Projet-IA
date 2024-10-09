from flask_sqlalchemy import SQLAlchemy
import logging as lg
import random

db = SQLAlchemy()

def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    lg.warning('database initialized')

class Player(db.Model) :
    __tablename__ = 'players'

    player_id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(25), nullable=True, unique=True)
    is_human = db.Column(db.Boolean, nullable=False)
    games = db.relationship("Game", back_populates="players")

    def __init__(self, is_human, nickname=None) :
        self.is_human = is_human
        self.nickname = nickname


class Game(db.Model) :
    __tablename__ = 'games'

    game_id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.SmallInteger, nullable=False)
    pos_player_1 = db.Column(db.String, nullable=False)
    pos_player_2 = db.Column(db.String, nullable=False)
    turn_player_1 = db.Column(db.Boolean, nullable=False)
    board_state = db.Column(db.String, nullable=False)
    winner_player_1 = db.Column(db.Boolean, nullable=True)
    player_1_id = db.Column(db.Integer, db.ForeignKey('players.player_id'))
    player_2_id = db.Column(db.Integer, db.ForeignKey('players.player_id'))
    players = db.relationship("Player", back_populates="games")

    def __init__(self, player_1, player_2, size) :
        self.size = size
        self.pos_player_1 = "0,0"
        self.pos_player_2 = str(size - 1) + "," + str(size - 1)
        self.turn_player_1 = random.choice([True, False])
        self.board_state = "1" + "0"*((size**2)-2) + "2"
        self.player_1_id = player_1
        self.player_2_id = player_2
