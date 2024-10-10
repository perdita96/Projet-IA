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

@app.route('/game')
def game():
    game = request.args.get('game')
    player_id = request.args.get('player_id')
    return render_template('game.html', game=game, player_id=player_id)

@app.route('/app.css')
def send_css():
    return render_template('app.css')

    """
    Vérifier si un joueur existe dans la base de données.

    Préconditions:
    - 'nickname' est une chaîne de caractères représentant le pseudo d'un joueur.
    - La base de données est accessible via 'db.session'.
    - Il faut que la fonction ait accès au modèle Player

    Postconditions:
    - Retourne True si un joueur avec ce pseudo existe dans la base de données.
    - Retourne False si aucun joueur avec ce pseudo n'est trouvé.
    """
def player_exists(nickname):
    if db.session.query(Player).filter_by(nickname=nickname).first() == None:
        return False
    return True

    """
    Renvoier l'ID du joueur ayant le pseudo donné.

    Préconditions:
    - 'nickname' doit être une chaîne de caractères représentant un pseudo existant dans la base de données.
    - La base de données est accessible via 'db.session'.
    - Il faut que la fonction ait accès au modèle Player

    Postconditions:
    - Retourne l'ID ('player_id') du joueur correspondant au pseudo.
    """
def id_searched_player(nickname):
    return db.session.query(Player).filter_by(nickname=nickname).first().player_id

    """
    Ajouter un nouveau joueur dans la base de données.

    Préconditions:
    - 'nickname' doit être une chaîne de caractères qui n'existe pas encore dans la base de données.
    - La base de données est accessible via 'db.session'.
    - Il faut que la fonction ait accès au modèle Player

    Postconditions:
    - Un nouveau joueur est ajouté à la base de données.
    """
def add_player(nickname): 
    new_player = Player(is_human= nickname!= 'IA', nickname=nickname) 
    db.session.add(new_player)  
    db.session.commit()

    """
    Créer une partie avec deux joueurs

    Préconditions:
    - 'data' doit être un dictionnaire contenant au moins deux champs 'player_1' et 'player_2' (pseudos des joueurs).

    Postconditions:
    - Si les joueurs n'existent pas dans la base de données, ils sont créés.
    - Une nouvelle partie est créée avec la taille de la grille spécifiée (5x5)
    - La partie est ajoutée et sauvegardée dans la base de données.
    """
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
    
        

    