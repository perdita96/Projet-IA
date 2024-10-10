<<<<<<< HEAD
<<<<<<< HEAD
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from .models import Player, db, Game
from .ai import get_move
from . import business
=======
from flask import Flask, render_template, redirect, url_for, flash
=======
from flask import Flask, render_template, redirect, url_for, request
>>>>>>> f27a56e (postCondition)
from BLOCKADE.models import Player, db, Game  # Assurez-vous d'importer db
>>>>>>> e71433e (Créer partie)
import config

app = Flask(__name__)
app.config.from_object(config)

<<<<<<< HEAD
db.init_app(app) 

#Post-conditions : La fonction renvoie le template index.html
=======
db.init_app(app)  # Ajoutez cette ligne pour l'initialisation

>>>>>>> e71433e (Créer partie)
@app.route('/')
def index():
    "return index template"
    return render_template('index.html')

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
#Pré-condition :
    #la requête est de type POST
    #Les données de la requête sont au format JSON
    #Les données de la requête contiennent les clés game, player et direction
#Post-condition:
    # Si le jeu n'existe pas, la fonction renvoie une erreur 404 avec un message "Game not found"
    # Si le joueur n'est pas partie du jeu, la fonction renvoie une erreur 403 avec un message "Player is not part of the game"
    # Si le mouvement n'est pas valide, la fonction renvoie une erreur 400 avec un message
    # Si le mouvement est valide, la fonction met à jour le jeu, fait jouer IA si c'est son tour et renvoie les données du jeu sous forme de JSON
    # Si le jeu est terminé, la fonction redirige vers la page ??
@app.route('/move', methods=[ 'POST'])
def move():
    data = request.get_json()
    game_id = data['game']
    player_id = data['player']
    direction = data['dir']
    
    game = db.session.query(Game).get(game_id)
    if game is None:
        return jsonify({"error": "Game not found"}), 404
=======
@app.route('/game')
def game():
    game = request.args.get('game')
    player_id = request.args.get('player_id')
    return render_template('game.html', game=game, player_id=player_id)
>>>>>>> d1f71e1 (ttt)

    if int(player_id) not in [int(game.player_1_id), int(game.player_2_id)]:
        return jsonify({"error": "Player is not part of the game"}), 403

    try:
        game = business.move(game, player_id, direction)
        if(game.turn_player_1):
            next_player_id = game.player_1_id
        else:
            next_player_id = game.player_2_id
        next_player = db.session.query(Player).get(next_player_id)
        #if (game.winner_player_1  is None and not next_player.is_human):
            #ai_move = get_move(updated_game)
            #updated_game = business.move(updated_game, ai, ai_move)
        db.session.commit()

        if  game.winner_player_1  is None:
            return jsonify({'boardState': game.board_state,'pos_player_1': game.pos_player_1,'pos_player_2': game.pos_player_2 })
        else:
            #a modifier quand on aura la page de fin
            return jsonify({"winner": game.winner_player_1 })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    


#Pré-conditions :
    #Les paramètres game et player_id sont présents dans l'URL
#Post-conditions :
    #La fonction renvoie le template game.html avec les paramètres game et player_id
@app.route('/game/<int:game_id>/<int:player_id>')
def game(game_id, player_id):
    # Chercher la game et le player dans la base de données
    game = db.session.query(Game).get(game_id)
    if game is None:
        return jsonify({"error": "Game not found"}), 404
    if player_id not in [game.player_1_id, game.player_2_id]:
        return jsonify({"error": "Player is not part of the game"}), 403
    return render_template('game.html', game=game, player_id=player_id)

#Post-conditions :
    # La fonction renvoie le fichier CSS app.css
@app.route('/static/<path:path>')
def send_static(path):
    return render_template('static', path)

####

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
=======
@app.route('/game')
def game():
    "return game template"
    return render_template('game.html', size=config.BOARD_SIZE)
=======
@app.route('/game/<game_state>/<player_id>', methods=['GET'])
def game(game_state, player_id):
    "return game template"
    return render_template('game.html')
>>>>>>> f27a56e (postCondition)

@app.route('/app.css')
def send_css():
    return render_template('app.css')

<<<<<<< HEAD

>>>>>>> e71433e (Créer partie)
=======
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
>>>>>>> f27a56e (postCondition)
def player_exists(nickname):
    if db.session.query(Player).filter_by(nickname=nickname).first() == None:
        return False
    return True

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> f27a56e (postCondition)
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

<<<<<<< HEAD
=======
def id_searched_player(nickname):
    return db.session.query(Player).filter_by(nickname=nickname).first().player_id

def add_player(nickname): 
    new_player = Player(is_human=True, nickname=nickname) 
    db.session.add(new_player)  
    db.session.commit()

@app.route('/createGame/<player_1_nickname>/<player_2_nickname>', methods=['GET'])
def create_game(player_1_nickname, player_2_nickname, size=config.BOARD_SIZE) :
>>>>>>> e71433e (Créer partie)
=======
>>>>>>> f27a56e (postCondition)
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
    
        

<<<<<<< HEAD
    
=======
    
    player_1_id = id_searched_player(player_1_nickname)
    player_2_id = id_searched_player(player_2_nickname)

    new_game = Game(player_1=player_1_id, player_2=player_2_id, size=size)
    db.session.add(new_game)
    db.session.commit()
    return redirect(url_for('index'))  

>>>>>>> e71433e (Créer partie)
=======
    
>>>>>>> f27a56e (postCondition)
