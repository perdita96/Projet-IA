from flask import Flask, render_template, request, jsonify
from . import Game, Player
from . import business
import config

app = Flask(__name__)

app.config.from_object(config)

@app.route('/')
def index():
    "return index template"
    return render_template('index.html')

@app.route('/move', methods=['GET', 'POST'])
def move():
    data = request.get_json()
    game_id = data['gameId']
    player = data['player']
    direction = data['direction']

    game = Game.query.get(game_id)
    if game is None:
        return jsonify({"error": "Game not found"}), 404

    if player not in [game.player_1, game.player_2]:
        return jsonify({"error": "Player is not part of the game"}), 403

    try:
        updated_game = business.move(game, player, direction)
        if(updated_game.turn_player_1):
            next_player_id = game.player_1_id
        else:
            next_player_id = game.player_2_id
        next_player = Player.query.get(next_player_id)
        #if not next_player.is_human:
            # ai_move = ai.move(updated_game)
            # updated_game = business.move(updated_game, ai, ai_move)
        #db.session.commit()
        return jsonify(updated_game)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# doit etre modifier
@app.route('/game', methods=['GET', 'POST'])
def game():
    data = request.get_json()
    player = data['player']
    #creer game
    game = createGame(player, config.BOARD_SIZE)
    #si joueur 1 est 1 ffaire jouer ia

    "return game template"
    return render_template('game.html', game, player);

@app.route('/app.css')
def send_css():
    return render_template('app.css')
