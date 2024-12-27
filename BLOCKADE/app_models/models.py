from flask_sqlalchemy import SQLAlchemy
import logging as lg
import random

#créer instance de la base de données
db = SQLAlchemy()

def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    lg.warning('database initialized')

class Qtable(db.Model):
    __tablename__ = 'qtable'

    state = db.Column(db.String(30), primary_key=True)
    ArrowUp = db.Column(db.Float, nullable=False)
    ArrowDown = db.Column(db.Float, nullable=False)
    ArrowRight = db.Column(db.Float, nullable=False)
    ArrowLeft = db.Column(db.Float, nullable=False)

    def __init__(self, state, ArrowUp=0 , ArrowDown=0, ArrowRight=0, ArrowLeft=0):
        self.state = state
        self.ArrowUp = ArrowUp
        self.ArrowDown = ArrowDown
        self.ArrowRight = ArrowRight 
        self.ArrowLeft = ArrowLeft

class PreviousStateAction(db.Model) :
    __tablename__ = 'previousStateAction'

    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'), primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'), primary_key=True)
    previous_state = db.Column(db.String(30))
    previous_action = db.Column(db.String(10))

    player = db.relationship("Player", foreign_keys=[player_id], back_populates="previous_state_action")
    game = db.relationship("Game", foreign_keys=[game_id], back_populates="previous_state_action")

    def __init__(self, game_id, player_id, previous_state, previous_action):
        self.game_id = game_id
        self.player_id = player_id
        self.previous_state = previous_state
        self.previous_action = previous_action



class Player(db.Model):
    __tablename__ = 'players'

    player_id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(25), nullable=True, unique=True)
    is_human = db.Column(db.Boolean, nullable=False)

    games_as_player_1 = db.relationship("Game", foreign_keys='Game.player_1_id', back_populates="player_1")
    
    games_as_player_2 = db.relationship("Game", foreign_keys='Game.player_2_id', back_populates="player_2")

    previous_state_action = db.relationship("PreviousStateAction", foreign_keys='PreviousStateAction.player_id', back_populates="player")



    def __init__(self, is_human, nickname=None):
        self.is_human = is_human
        self.nickname = nickname


class Game(db.Model):
    """
        Winner peut valoir : 
            . 1 --> le joueur 1 à gagné
            . 2 --> le joueur 2 à gagné
            . -1 --> les joueurs sont à égalité
    """
    __tablename__ = 'games'

    game_id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.SmallInteger, nullable=False)
    pos_player_1 = db.Column(db.String, nullable=False)
    pos_player_2 = db.Column(db.String, nullable=False)
    turn_player_1 = db.Column(db.Boolean, nullable=False)
    board_state = db.Column(db.String, nullable=False)
    winner = db.Column(db.SmallInteger, nullable=True) 
    player_1_id = db.Column(db.Integer, db.ForeignKey('players.player_id'))
    player_2_id = db.Column(db.Integer, db.ForeignKey('players.player_id'))

    player_1 = db.relationship("Player", foreign_keys=[player_1_id], back_populates="games_as_player_1")
    player_2 = db.relationship("Player", foreign_keys=[player_2_id], back_populates="games_as_player_2")

    previous_state_action = db.relationship("PreviousStateAction", foreign_keys='PreviousStateAction.game_id', back_populates="game")


    def __init__(self, player_1, player_2, size):
        self.size = size
        self.pos_player_1 = "0,0"
        self.pos_player_2 = str(size - 1) + "," + str(size - 1)
        self.turn_player_1 = random.choice([True, False])
        self.board_state = "1" + "0"*((size**2)-2) + "2"
        self.player_1_id = player_1
        self.player_2_id = player_2
        self.winner = 0