from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from .models import Player, db, Game  # Assurez-vous d'importer db
from . import business
import config

app = Flask(__name__)

app.config.from_object(config)

@app.route('/')
def index():
    "return index template"
    return render_template('index.html')

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
        #if not next_player.is_human:
            # ai_move = ai.move(updated_game)
            # updated_game = business.move(updated_game, ai, ai_move)
        db.session.commit()
        return jsonify(game)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# doit etre modifier
@app.route('/game')
def game():
    return render_template('game.html');

@app.route('/app.css')
def send_css():
    return render_template('app.css')
