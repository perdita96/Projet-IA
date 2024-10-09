from flask import Flask, render_template, redirect, url_for, flash
from BLOCKADE.models import Player, db, Game  # Assurez-vous d'importer db
import config

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)  # Ajoutez cette ligne pour l'initialisation

@app.route('/')
def index():
    "return index template"
    return render_template('index.html')

@app.route('/game')
def game():
    "return game template"
    return render_template('game.html', size=config.BOARD_SIZE)

@app.route('/app.css')
def send_css():
    return render_template('app.css')


def player_exists(nickname):
    if db.session.query(Player).filter_by(nickname=nickname).first() == None:
        return False
    return True

def id_searched_player(nickname):
    return db.session.query(Player).filter_by(nickname=nickname).first().player_id

def add_player(nickname): 
    new_player = Player(is_human=True, nickname=nickname) 
    db.session.add(new_player)  
    db.session.commit()

@app.route('/createGame/<player_1_nickname>/<player_2_nickname>', methods=['GET'])
def create_game(player_1_nickname, player_2_nickname, size=config.BOARD_SIZE) :
    if not player_exists(player_1_nickname) :
        add_player(player_1_nickname)
    if not player_exists(player_2_nickname) :
        add_player(player_2_nickname)
    
    player_1_id = id_searched_player(player_1_nickname)
    player_2_id = id_searched_player(player_2_nickname)

    new_game = Game(player_1=player_1_id, player_2=player_2_id, size=size)
    db.session.add(new_game)
    db.session.commit()
    return redirect(url_for('index'))  

