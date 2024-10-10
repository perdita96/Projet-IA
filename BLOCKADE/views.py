from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from .models import Player, db, Game
from . import business
import config

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app) 

#Post-conditions : La fonction renvoie le template index.html
@app.route('/')
def index():
    "return index template"
    return render_template('index.html')

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
    direction = data['direction']
    
    game = db.session.query(Game).get(game_id)
    if game is None:
        return jsonify({"error": "Game not found"}), 404

    if player_id not in [game.player_1, game.player_2]:
        return jsonify({"error": "Player is not part of the game"}), 403

    try:
        game = business.move(game, player_id, direction)
        if(game.turn_player_1):
            next_player_id = game.player_1_id
        else:
            next_player_id = game.player_2_id
        next_player = db.session.query(Player).get(next_player_id)
        #if (game.winner_player_1  is None and not next_player.is_human):
            # ai_move = ai.move(updated_game)
            # updated_game = business.move(updated_game, ai, ai_move)
        db.session.commit()
        if  game.winner_player_1  is None:
            return jsonify(game)
        else:
            #a modifier quand on aura la page de fin
            return jsonify({"winner": game.winner_player_1 })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

#Pré-conditions :
    #La requête est de type GET
    #Les paramètres game et player_id sont présents dans l'URL
#Post-conditions :
    #La fonction renvoie le template game.html avec les paramètres game et player_id
@app.route('/game')
def game():
    game = request.args.get('game')
    player_id = request.args.get('player_id')
    return render_template('game.html', game=game, player_id=player_id)

#Post-conditions :
    # La fonction renvoie le fichier CSS app.css
@app.route('/app.css')
def send_css():
    return render_template('app.css')

####

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
    new_player = Player(is_human=True, nickname=nickname) 
    db.session.add(new_player)  
    db.session.commit()

#précondition : les pseudos de deux joueurs sont données en argument même si il n'existe pas dans la DB. La taille de la grille du jeu peut aussi être donnée
#postcondition : une partie de la taille passée en argument ou de 5X5 par défaut est créée avec les joueurs passés en arguments
@app.route('/createGame', methods=['GET'])
def create_game(player_1_nickname, player_2_nickname='IA') :
    if not player_exists(player_1_nickname) :
        add_player(player_1_nickname)
    if not player_exists(player_2_nickname) :
        add_player(player_2_nickname)
    
    player_1_id = id_searched_player(player_1_nickname)
    player_2_id = id_searched_player(player_2_nickname)

    new_game = Game(player_1=player_1_id, player_2=player_2_id, size=config.BOARD_SIZE)
    db.session.add(new_game)
    db.session.commit()

    return redirect(url_for('game', game=new_game, player_id=player_1_id))
    

