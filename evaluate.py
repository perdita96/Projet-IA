from BLOCKADE import app
from BLOCKADE.app_models.models import *
from BLOCKADE.app_models.util import *
from BLOCKADE.business import move
from BLOCKADE.ai import get_move, end_game, explore

import config
import sys

def set_eps_config(eps):
    with open('config.py', 'r') as f:
       lines = f.readlines()
    
    with open('config.py', 'w') as f:
        for line in lines:
            if line.startswith('EPS ='):
                f.write(f"EPS = {eps}\n")
            else:
                f.write(line)

def get_player_move(game, player_id):
    match player_id:
        case game.player_1.id:
            move = explore(game, "2")
        case game.player_2.id:
            move = get_move(game, "2")
        case _:
            raise ValueError('Invalid Player id')
    return move

def play_game(ai_id, random_id):
    game = Game(player_1=random_id, player_2=ai_id, size=config.BOARD_SIZE)
    db.session.add(game)
    db.session.commit()

    while(game.winner == 0) :
        current_player = game.player_1 if game.turn_player_1 else game.player_2
        game = move(game, current_player.id, get_player_move(game, current_player.id))
        db.session.commit()
    
    end_game(game, "2")

def evaluate_model(nb_games, nb_wins):
    win_pct = (nb_wins / nb_games) * 100
    nb_loses = nb_games - nb_wins
    print('-' * 20)
    print('\tRANDOM' + (' ' * 10) + 'AI')
    print(f'\tGames won : {nb_loses}\t\tGames won : {nb_wins}')
    print(f'\tGames lost : {nb_wins}\t\tGames lost : {nb_loses}')
    print(f'\tWin percentage : {1 - win_pct:.2f}%\t\tWin percentage : {win_pct:.2f}')
    print(f'\tLose percentage : {win_pct:.2f}%\t\tLose percentage : {1 - win_pct:.2f}')
    print()
    print(f'\t\tBEST AI : {'RANDOM' if win_pct < 50 else 'AI' if win_pct > 50 else 'NONE'}')


if __name__ == '__main__':
    min_games = 50
    max_games = 10000

    match len(sys.argv):
        case 1: 
            nb_games = 1000
        case 2:
            nb_games = int(sys.argv[1])
            if not min_games <= nb_games <= max_games:
                raise ValueError(f'The number of games required for evaluation must be between {min_games} and {max_games}')
        case _:
            raise ValueError(f'Either one or no argument can be passed')
    
    with app.app_context():
        original_eps = config.EPS
        set_eps_config(0)

        if not player_exists('Random'):
            add_player('Random')
        if not player_exists('IA'):
            raise ValueError("L'IA n'existe pas")

        random_id = id_searched_player('Random')
        ai_id = id_searched_player('IA')

        nb_wins = 0
        for _ in range(nb_games):
            winner = play_game(ai_id, random_id)
            if winner == 2:
                nb_wins += 1
        
        evaluate_model(nb_games, nb_wins)

        set_eps_config(original_eps)