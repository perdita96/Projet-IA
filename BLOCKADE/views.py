from flask import Flask, render_template, redirect, url_for, request
from BLOCKADE.models import Player, db, Game  # Assurez-vous d'importer db
import config

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)  # Ajoutez cette ligne pour l'initialisation

@app.route('/')
def index():
    "return index template"
    return render_template('index.html')

@app.route('/game/<game_state>/<player_id>', methods=['GET'])
def game(game_state, player_id):
    "return game template"
    return render_template('game.html')

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

#précondition : les pseudos de deux joueurs sont données fourni en JSON même si il n'existe pas dans la DB. La taille de la grille du jeu peut aussi être donnée
#postcondition : une partie de la taille passée en argument ou de 5X5 par défaut est créée avec les joueurs passés en arguments
@app.route('/createGame', methods=['POST','GET'])
def create_game() :
    
    request_data = request.get_json()

    player_1_nickname = request_data['player_1']

    if 'player_2' in request_data :
        player_2_nickname = request_data['player_2']
    else : 
        player_2_nickname = 'IA'

    if not player_exists(player_1_nickname) :
        add_player(player_1_nickname)
    if not player_exists(player_2_nickname) :
        add_player(player_2_nickname)
        
    player_1_id = id_searched_player(player_1_nickname)
    player_2_id = id_searched_player(player_2_nickname)

    new_game = Game(player_1=player_1_id, player_2=player_2_id, size=config.BOARD_SIZE)
    db.session.add(new_game)
    db.session.commit()

    return redirect(url_for('game', game_state='new_game', player_id=player_1_id))
    
        

    