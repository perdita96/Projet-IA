from BLOCKADE import app
from BLOCKADE.app_models.models import *
from BLOCKADE.app_models.util import *
from BLOCKADE.business import move
from BLOCKADE.ai import get_move, end_game
import config

def play_game(game) :
    while(game.winner == 0) :

        current_player =  game.player_1 if game.turn_player_1 else game.player_2

        game = move(game, current_player.id,get_move(game, current_player.id))

        db.session.commit() #ici ? 

    end_game(game,current_player.id)

    db.session.commit()

if __name__ == "__main__":

    nb_games_wanted = int(input("Combien de partie voulez-vous jouer : ")) # j'ai ajouter la converssion

    #démarrer l'ap ==> BASE DE DONNEES
    app.run()

    if not player_exists('IA'):
        add_player('IA')
        
    ai_id = id_searched_player('IA')

    #si parti non terminée -> reprend et finir
    #last_game = db.session.query(Game).order_by(Game.id.desc()).first()
    last_game = db.session.query(Game).filter(Game.player_1 == ai_id, Game.player_2 == ai_id).first() # c'est pas mieux?

    if last_game : 
        if last_game.winner == 0 : 
            #fonction jouer game
            play_game(last_game)

    nb_games_played = db.session.query(Game).filter(Game.player_1 == ai_id, Game.player_2 == ai_id).count()

    i_game = 0
    while nb_games_played < config.MAX_GAMES and i_game < nb_games_wanted : 

        new_game = Game(player_1=ai_id, player_2=ai_id, size=config.BOARD_SIZE)
        db.session.add(new_game)
        db.session.commit()

        play_game(new_game)

        i_game += 1

    #si nb_games_played = MAX_GAMES -> lancer l'évaluation contre elle même et contre random



