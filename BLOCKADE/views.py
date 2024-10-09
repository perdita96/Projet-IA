from flask import Flask, render_template, redirect, url_for, jsonify
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

#précondition : le pseudo d'un joueur est passé en argument 
#postcondition : si le joueur est présent dans la base de données la fonction retourne vrai sinon faux
def player_exists(nickname):
    if db.session.query(Player).filter_by(nickname=nickname).first() == None:
        return False
    return True

#précondition : le pseudo du joueur doit exister dans la base de données
#postcondition : L'id du joueur ayant le pseudo en question est renvoyé
def id_searched_player(nickname):
    return db.session.query(Player).filter_by(nickname=nickname).first().player_id

#précondition : le pseudo d'un joueur qui n'est pas encore présent dans la base de données est fourni en argument
#postcondition : le joueur est rajouté à la base de données
def add_player(nickname): 
    new_player = Player(is_human= nickname!= 'IA', nickname=nickname) 
    db.session.add(new_player)  
    db.session.commit()

#précondition : les pseudos de deux joueurs sont données en argument même si il n'existe pas dans la DB. La taille de la grille du jeu peut aussi être donnée
#postcondition : une partie de la taille passée en argument ou de 5X5 par défaut est créée avec les joueurs passés en arguments
@app.route('/createGame/<player_1_nickname>/', methods=['GET'])
@app.route('/createGame/<player_1_nickname>/<player_2_nickname>', methods=['GET'])
def create_game(player_1_nickname, player_2_nickname='IA', size=config.BOARD_SIZE) :
    if not player_exists(player_1_nickname) :
        add_player(player_1_nickname)
    if not player_exists(player_2_nickname) :
        add_player(player_2_nickname)
    
    player_1_id = id_searched_player(player_1_nickname)
    player_2_id = id_searched_player(player_2_nickname)

    new_game = Game(player_1=player_1_id, player_2=player_2_id, size=config.BOARD_SIZE)
    db.session.add(new_game)
    db.session.commit()

    """
    game_state = {
        'game_id': new_game.game_id,
        'board_state' : new_game.board_state,
        'pos_player_1' : new_game.pos_player_1,
        'pos_player_2' : new_game.pos_player_2,
        'turn_player_1' : new_game.turn_player_1,
        'winner_player_1' : new_game.winner_player_1
    }
    """
    return redirect(url_for('game', game_state=new_game, player_id=player_1_id))  
    #return jsonify(game_state)
    

