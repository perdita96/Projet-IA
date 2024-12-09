from BLOCKADE import app
from BLOCKADE.app_models.models import *
from BLOCKADE.app_models.util import *
from BLOCKADE.business import move
from BLOCKADE.ai import get_move, end_game, update_epsilon
import config

def play_game(game) :
    """
    Gère le déroulement d'une partie entre une IA et elle même jusqu'à ce qu'un gagnant soit déterminé.

    Pré-conditions :

        - L'objet game doit être une instance de la classe Game.

        - L'objet game doit avoir les attributs suivants :
            - winner : un entier (0 si aucun gagnant, sinon l'identifiant du gagnant)
            - player_1 : l'identifiant du joueur 1
            - player_2 : l'identifiant du joueur 2
            - turn_player_1 : un booléen indiquant si c'est le tour du joueur 1

    Post-conditions 
        - La partie est jouée jusqu'à ce qu'un gagnant soit déterminé.
        - L'état du jeu est mis à jour dans la base de données après chaque mouvement. 
        - Peut renvoyer une erreur provenant de la fonction move

    """
    current_player_id =  game.player_1_id if game.turn_player_1 else game.player_2_id

    while(game.winner == 0) :  
        try : 
            print(current_player_id)
            game = move(game, current_player_id, get_move(game, current_player_id))
            db.session.commit()

            current_player_id =  game.player_1_id if game.turn_player_1 else game.player_2_id
            
        except ValueError as e:
            raise e
        
    end_game(game, current_player_id)

def trainning() : 
    """
    Gère le processus d'entraînement de l'IA en jouant un certain nombre de parties.

    Pré-conditions :
        - La classe Game doit être définie et accessible.
        - Les fonctions player_exists, add_player, id_searched_player, play_game, et update_epsilon doivent être définies.
        - Un nombre de parties à jouer est demandé à l'utilisateur, il doit être un entier positif.

    Post-conditions :
        - Si le joueur "IA" n'existe pas, il est créé.
        - L'IA joue un nombre spécifié de parties contre elle-même sans dépasser le nombre de parties maximum.
        - L'état des parties est enregistré dans la base de données.
        - La valeur d'epsilon est mise à jour toutes les 500 parties jouées.
        - Peut renvoyer une erreur provenant de la fonction play_game

    """
    if not player_exists('IA'):
        add_player('IA')
    if not player_exists('Alice') :
        add_player('Alice')
        
    ai_id = id_searched_player('IA')
    alice_id = id_searched_player('Alice')


    last_game = db.session.query(Game).filter(Game.player_1 == ai_id, Game.player_2 == ai_id).first()

    if last_game : 
        if last_game.winner == 0 : 
            try : 
                play_game(last_game)
            except ValueError as e:
                raise e

    nb_games_played = db.session.query(Game).filter(Game.player_1_id == ai_id, Game.player_2_id == alice_id).count()

    print(f"{nb_games_played}/{config.MAX_GAMES} parties jouées")
    nb_games_wanted = int(input("Combien de partie voulez-vous jouer : "))

    i_game = 0
    while nb_games_played < config.MAX_GAMES and i_game < nb_games_wanted : 

        new_game = Game(player_1=ai_id, player_2=alice_id, size=config.BOARD_SIZE)
        db.session.add(new_game)
        db.session.commit()

        try : 
            play_game(new_game)
        except ValueError as e:
            raise e

        i_game += 1
        nb_games_played += 1

        if nb_games_played % 500 == 0: #utiliser une formule qui déterminer 500 pour que ce soit adaptatif ? Genre (config.MAX_GAMES / 400) à la place de 500 ?
            update_epsilon()

    print(f"{nb_games_played}/{config.MAX_GAMES} parties jouées")

if __name__ == "__main__":

    with app.app_context():
        try  :
            trainning()
        except ValueError as e:
            print("error : " + str(e))
            

    

    #si nb_games_played = MAX_GAMES -> lancer l'évaluation contre elle même et contre random



