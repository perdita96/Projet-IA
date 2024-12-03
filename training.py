from BLOCKADE import app
from BLOCKADE.app_models.models import *
from BLOCKADE.app_models.util import *
from BLOCKADE.business import move
from BLOCKADE.ai import get_move, end_game
import config

def play_game(game) :
    while(game.winner == 0) :

        current_player =  game.player_1 if game.turn_player_1 else game.player_

        game = move(game, current_player.id,get_move(game, current_player.id))

        db.session.commit() #ici ? 

    end_game(game,current_player.id)

    db.session.commit()

if __name__ == "__main__":

    nb_games_wanted = input("Combien de partie voulez-vous jouer : ")

    #démarrer l'ap ==> BASE DE DONNEES
    app.run()

    if not player_exists('IA'):
        add_player('IA')
        
    ai_id = id_searched_player('IA')

    #si parti non terminée -> reprend et finir
    last_game = db.session.query(Game).order_by(Game.id.desc()).first()

    if last_game : 
        if last_game.winner == 0 : 
            #fonction jouer game
            play_game(last_game)

    nb_games_played = db.session.query(Game).count()

    i_game = 0
    while nb_games_played < config.MAX_GAMES and i_game < nb_games_wanted : 

        new_game = Game(player_1=ai_id, player_2=ai_id, size=config.BOARD_SIZE)
        db.session.add(new_game)
        db.session.commit()

        play_game(new_game)

        i_game += 1



