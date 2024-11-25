from flask import Flask, render_template, request, jsonify
from .app_models.models import *
from .app_models.util import *
from .ai import*
from . import business
import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app) 


@app.route('/')
def index():
    """
    Route qui renvoie la page d'accueil 

    Post-conditions : La fonction renvoie le template index.html
    """
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    """
    Route qui permet de traiter le mouvement d'un joueur sur le plateau du jeu

    Pré-conditions :
        la requête est de type POST
        Les données de la requête sont au format JSON
        Les données de la requête contiennent les clés game, player et direction
    Post-conditions :
        Si le jeu n'existe pas, la fonction renvoie une erreur 404 avec un message "Game not found"
        Si le joueur n'est pas partie du jeu, la fonction renvoie une erreur 403 avec un message "Player is not part of the game"
        Si le mouvement n'est pas valide, la fonction renvoie une erreur 400 avec un message
        Si le mouvement est valide, la fonction met à jour le jeu, fait jouer IA si c'est son tour et renvoie les données du jeu sous forme de JSON
        Si le jeu est terminé, la fonction redirige vers la page ??
    """
    data = request.get_json()
    game_id = data['game']
    player_id = data['player']
    direction = data['dir']
    
    game = db.session.query(Game).get(game_id)
    if game is None:
        return jsonify({"error": "Game not found"}), 404

    if int(player_id) not in [int(game.player_1_id), int(game.player_2_id)]:
        return jsonify({"error": "Player is not part of the game"}), 403

    try:
        game = business.move(game, player_id, direction)
        if game.turn_player_1: 
            next_player_id = game.player_1_id
        else:
            next_player_id = game.player_2_id
        next_player = db.session.query(Player).get(next_player_id)
        
        if not game.winner and not next_player.is_human:
            game = business.move(game, next_player.player_id, get_move(game, next_player.player_id))
        db.session.commit()

        if not game.winner:
            return jsonify({'boardState': game.board_state, 'pos_player_1': game.pos_player_1, 'pos_player_2': game.pos_player_2})
        else:
            if next_player.is_human:
                end_game(game,next_player)
            if game.winner == -1:
                status = "draw"
            if game.winner == 1 and int(game.player_1_id) == int(player_id) or game.winner == 2 and int(game.player_2_id) == int(player_id):
                status = "win"
            if game.winner == 2 and int(game.player_1_id) == int(player_id) or game.winner == 1 and int(game.player_2_id) == int(player_id):
                status = "lose"
            return jsonify({'url': 'endGame', 'status': status, 'player_id': player_id})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    

@app.route('/game/<int:game_id>/<int:player_id>')
def game(game_id, player_id): 
    """
    Route qui retourne le template de la partie

    Pré-conditions :
        Les paramètres game et player_id sont présents dans l'URL
    Post-conditions :
        Fait jouer l'IA si besoin
        Sinon la fonction renvoie le template game.html avec les paramètres game et player_id
    """
    game = db.session.query(Game).get(game_id)
    if game is None:
        return jsonify({"error": "Game not found"}), 404
    if player_id not in [game.player_1_id, game.player_2_id]:
        return jsonify({"error": "Player is not part of the game"}), 403
    
    if game.turn_player_1: 
        current_player_id = game.player_1_id
    else:
        current_player_id = game.player_2_id
    current_player = db.session.query(Player).get(current_player_id)

    if not game.winner and not current_player.is_human: 
        game = business.move(game, current_player.player_id, get_move(game, current_player.player_id)) 
        db.session.commit()
    return render_template('game.html', game=game, player_id=player_id)         

@app.route('/static/<path:path>')
def send_static(path):
    """
    Post-conditions :
        La fonction renvoie le fichier CSS
    """
    return render_template('static', path)

@app.route('/createGame', methods=['POST'])
def create_game():
    """
    Route pour créer une partie 

    Préconditions:
    - 'data' doit être un dictionnaire contenant au moins le champ 'player_1' (pseudos du joueurs)
    - 'player_2' est optionnel dans le cas ou il n'y à pas de player 2, il s'agit d'un partie contre l'IA

    Post-conditions:
    - Si les joueurs n'existent pas dans la base de données, ils sont créés.
    - Une nouvelle partie est créée avec la taille de la grille spécifiée (5x5)
    - La partie est ajoutée et sauvegardée dans la base de données.
    """
    request_data = request.get_json()

    player_1_nickname = request_data['player_1']

    if 'player_2' in request_data:
        player_2_nickname = request_data['player_2']
    else : 
        player_2_nickname = 'IA'

    if not player_exists(player_1_nickname):
        add_player(player_1_nickname)
    if not player_exists(player_2_nickname):
        add_player(player_2_nickname)
        
    player_1_id = id_searched_player(player_1_nickname)
    player_2_id = id_searched_player(player_2_nickname)

    new_game = Game(player_1=player_1_id, player_2=player_2_id, size=config.BOARD_SIZE)
    db.session.add(new_game)
    db.session.commit()

    return jsonify({'game_id': new_game.game_id, 'player_id': player_1_id})


@app.route('/endGame/<string:status>/<int:player_id>')
def end_game(status, player_id):
    """
    Route qui retourne le template de fin de jeu qui indique le gagnant

    Pré-conditions:
        - player_id doit être un entier qui identifie le joueur
        - is_winner doit être un booléen qui indique si le joueur player_id a gagné

    Post-conditions:
        - retourne la route à prendre
        - retourne le booléen qui indique si on a gagné ainsi que l'id du joueur
    """
    return render_template('endGame.html', status=status, player_id=player_id)