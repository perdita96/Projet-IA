from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from .models import Player, db, Game
from .ai import get_move
from . import business
import config

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app) 

"""
Post-conditions : La fonction renvoie le template index.html
"""
@app.route('/')
def index():
    "return index template"
    return render_template('index.html')

"""
Pré-condition :
    la requête est de type POST
    Les données de la requête sont au format JSON
    Les données de la requête contiennent les clés game, player et direction
Post-condition:
    Si le jeu n'existe pas, la fonction renvoie une erreur 404 avec un message "Game not found"
    Si le joueur n'est pas partie du jeu, la fonction renvoie une erreur 403 avec un message "Player is not part of the game"
    Si le mouvement n'est pas valide, la fonction renvoie une erreur 400 avec un message
    Si le mouvement est valide, la fonction met à jour le jeu, fait jouer IA si c'est son tour et renvoie les données du jeu sous forme de JSON
    Si le jeu est terminé, la fonction redirige vers la page ??
"""
@app.route('/move', methods=[ 'POST'])
def move():
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
        if(game.turn_player_1): #quelle interêt?
            next_player_id = game.player_1_id
        else:
            next_player_id = game.player_2_id
        next_player = db.session.query(Player).get(next_player_id)
        
        if  game.winner_player_1 is None:
            if not game.turn_player_1 :
                direction = get_move()
                while not is_move_possible(game, game.player_2_id, direction) : 
                    direction = get_move()
                business.move(game,game.player_2_id,direction)
        db.session.commit()

        if  game.winner_player_1  is None:
            return jsonify({'boardState': game.board_state,'pos_player_1': game.pos_player_1,'pos_player_2': game.pos_player_2 })
        else:
            #a modifier quand on aura la page de fin
            return jsonify({"winner": game.winner_player_1,'boardState': game.board_state,'pos_player_1': game.pos_player_1,'pos_player_2': game.pos_player_2 })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
"""
Pré-conditions :
    Les paramètres game et player_id sont présents dans l'URL
Post-conditions :
    Si la game est finie la fonction renvoie vers la page ???
    Fait jouer l'IA si besoin
    Si sinon la fonction renvoie le template game.html avec les paramètres game et player_id
"""
@app.route('/game/<int:game_id>/<int:player_id>')
def game(game_id, player_id): #pas moyen de sauvegarder player_1_id dans la page html?  Car sinon inutile ici
    game = db.session.query(Game).get(game_id)
    if game is None:
        return jsonify({"error": "Game not found"}), 404
    if player_id not in [game.player_1_id, game.player_2_id]:
        return jsonify({"error": "Player is not part of the game"}), 403
    if game.winner_player_1 == None : 
        if not game.turn_player_1 :
            move = get_move()
            while not is_move_possible(game, game.player_2_id, move) : 
                move = get_move()

            business.move(game,game.player_2_id,move) #pas besoin de faire de return car muable + comment gérer l'exception (devrait pas y avoir d'erreur)?
            db.session.commit()
    return render_template('game.html', game=game, player_id=player_id)
            

"""
Post-conditions :
    La fonction renvoie le fichier CSS
"""
@app.route('/static/<path:path>')
def send_static(path):
    return render_template('static', path)

"""
Post-conditions :
    L'id du joueur qui fait le mouvement doit être l'id d'un joueur présent dans la game
    Le mouvement doit être [ArrowUp, ArrowDown,ArrowLeft,ArrowRight]
"""
def is_move_possible(game, player_id, move) : #fusioner avec get_move dans ai.py? + le tant que is_move_possible?
    board_state = game.board_state
    size = game.size
    is_possible = True

    if player_id == game.player_1_id : 
        current_player = "1"
        current_pos = game.pos_player_1
    else :
        current_player = "2"
        current_pos = game.pos_player_2

    x, y = map(int, current_pos.split(","))

    if move == "ArrowUp":
        new_x, new_y = x - 1, y
    elif move == "ArrowDown":
        new_x, new_y = x + 1, y
    elif move == "ArrowLeft":
        new_x, new_y = x, y - 1
    elif move == "ArrowRight":
        new_x, new_y = x, y + 1

    is_possible = (0 <= new_x < size) and (0 <= new_y < size)
    if is_possible : 
        target_case = board_state[new_x * size + new_y]
        is_possible = (target_case == "0" or target_case == current_player)
        
    return is_possible
              
    
"""
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
Préconditions:
- 'data' doit être un dictionnaire contenant au moins deux champs 'player_1' et 'player_2' (pseudos des joueurs).

Postconditions:
- Si les joueurs n'existent pas dans la base de données, ils sont créés.
- Une nouvelle partie est créée avec la taille de la grille spécifiée (5x5)
- La partie est ajoutée et sauvegardée dans la base de données.
"""
@app.route('/createGame', methods=['POST'])
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

    return jsonify({'game_id': new_game.game_id, 'player_id': player_1_id})