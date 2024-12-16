from BLOCKADE import app
from BLOCKADE.app_models.models import *
from BLOCKADE.app_models.util import *
from BLOCKADE.business import move
from BLOCKADE.ai import get_move, end_game_ai, explore

import config
import sys

def set_eps_config(eps):
    """
    Modifie la valeur de l'epsilon dans le fichier de config

    Pré-conditions :
        - eps est un entier positif compris entre 0 et 1
    """
    with open('config.py', 'r') as f:
       lines = f.readlines()
    
    with open('config.py', 'w') as f:
        for line in lines:
            if line.startswith('EPS ='):
                f.write(f"EPS = {eps}\n")
            else:
                f.write(line)

def get_player_move(game, player_id):
    """
    Renvoie le mouvement du joueur

    Pré-conditions : 
        - game est la Game actuelle
        - player_id est l'id du joueur dont c'est le tour de jouer

    Post-conditions :
        - Renvoie un mouvement dont la valeur peut être ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown']
        - Lève une exception si le player_id est invalide
    """
    match player_id:
        case game.player_1_id :
            move = explore(game, player_id)
        case game.player_2_id:
            move = get_move(game, player_id)
        case _:
            raise ValueError('Invalid Player id')
    return move

def play_game(ai_id, random_id, ia_is_first):
    """
    Crée une game et fait jouer l'IA contre un random

    Pré-conditions : 
        - ai_id est l'id du joueur 'IA'
        - random_id est l'id du joueur 'Random'
        - ia_is_first determine si l'ia comance ou non

    Post-conditions : 
        - la partie est ajoutée en db et la QTable de l'IA est mise à jour
    """
    game = Game(player_1=random_id, player_2=ai_id, size=config.BOARD_SIZE)
    game.turn_player_1 = not ia_is_first
    db.session.add(game)
    db.session.commit()

    while(game.winner == 0) :
        current_player = game.player_1 if game.turn_player_1 else game.player_2
        game = move(game, current_player.player_id, get_player_move(game, current_player.player_id))
        db.session.commit()
    
    end_game_ai(game, game.player_2.player_id)

    return game.winner

def evaluate_model(nb_games, nb_wins, ia_is_first):
    """
    Affiche les résultats de l'évaluation
        Dont :
        - Le nombre de parties gagnées et perdues par chaque joueur
        - Le pourcentage de parties gagnées et perdues par chaque joueur
        - Le joueur qui a le meilleur score

        Pré-conditions : 
        - nb_game est le nombre de partie jouer
        - nb_wins est le nombre de partie gagné par l'ia
        - ia_is_first determine si l'ia comance ou non


    Pré-conditions :
        - nb_games est le nombre total de parties jouées
        - nb_wins est le nombre de parties gagnées par l'IA
    """
    win_pct = (nb_wins / nb_games) * 100
    nb_loses = nb_games - nb_wins
    print('-' * 20)
    print('ia commence' if ia_is_first else 'random commence')
    print('\tRANDOM' + (' ' * 10) + 'AI')
    print(f'\tGames won : {nb_loses}\t\tGames won : {nb_wins}')
    print(f'\tGames lost : {nb_wins}\t\tGames lost : {nb_loses}')
    print(f'\tWin percentage : {100 - win_pct:.2f}%\t\tWin percentage : {win_pct:.2f}')
    print(f'\tLose percentage : {win_pct:.2f}%\t\tLose percentage : {100 - win_pct:.2f}')
    print()
    print(f'\t\tBEST AI : {'RANDOM' if win_pct < 50 else 'AI' if win_pct > 50 else 'NONE'}')


if __name__ == '__main__':
    min_games = 5
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
        for _ in range(nb_games/2):
            winner = play_game(ai_id, random_id,True)
            if winner == 2:
                nb_wins += 1
        
        evaluate_model(nb_games/2, nb_wins,True)

        nb_wins = 0
        for _ in range(nb_games/2):
            winner = play_game(ai_id, random_id,False)
            if winner == 2:
                nb_wins += 1
        
        evaluate_model(nb_games/2, nb_wins,False)

        set_eps_config(original_eps)