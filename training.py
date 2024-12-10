from BLOCKADE import app
from BLOCKADE.app_models.models import *
from BLOCKADE.app_models.util import *
from BLOCKADE.business import move
from BLOCKADE.ai import get_move, end_game_ai
import config
import random

def update_epsilon():
    """
    Met à jour la valeur d'epsilon dans le fichier de configuration.

    Pré-conditions :
        - Présence d'un fichier config.py avec l'epsilon

    Post-conditions :
        - l'epsilon a été mis à jour dans le fichier config.py
    """
    current_epsilon = config.EPS
    new_epsilon = current_epsilon * config.DECAY_RATE

    new_epsilon = max(new_epsilon, config.MIN_EPSILON)

    config.EPS = new_epsilon

    with open('config.py', 'r') as f:
       lines = f.readlines()
    
    with open('config.py', 'w') as f:
        for line in lines:
            if line.startswith('EPS ='):
                f.write(f"EPS = {new_epsilon}\n")
            else:
                f.write(line)

    print(f"Epsilon mis à jour de {current_epsilon} à {new_epsilon}")

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
            game = move(game, current_player_id, get_move(game, current_player_id))
            db.session.commit()

            current_player_id =  game.player_1_id if game.turn_player_1 else game.player_2_id
            
        except ValueError as e:
            raise e
        
    end_game_ai(game, game.player_1_id)
    end_game_ai(game, game.player_2_id)

def training() : 
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

    last_game = db.session.query(Game).filter(Game.player_1_id == ai_id, Game.player_2_id == alice_id).first()

    if last_game : 
        if last_game.winner == 0 : 
            try : 
                play_game(last_game)
            except ValueError as e:
                raise e

    nb_games_played = db.session.query(Game).filter(Game.player_1_id == ai_id, Game.player_2_id == alice_id).count()

    print(f"{nb_games_played}/{config.MAX_GAMES} parties jouées")
    nb_games_wanted = int(input("Combien de partie voulez-vous jouer : "))

    phrases_of_encouragement  = [
        "On n'y est presque !",
        "L'entraînement porte ses fruits !",
        "Ne vous découragez pas !",
        "Chaque pas compte !",
        "Vous pouvez le faire !",
        "Continuez comme ça, c'est impressionnant !",
        "Vous êtes sur la bonne voie !",
        "Courage, les efforts paient toujours !",
        "Restez concentré, vous y arriverez !",
        "Bravo pour votre détermination !",
        "Le succès est à portée de main !",
        "Ne lâchez rien, vous êtes capable de tout !",
        "Petit à petit, l'oiseau fait son nid !",
        "Vous progressez à chaque instant !",
        "Votre travail acharné porte ses fruits !",
        "Vous faites des merveilles !",
        "Restez motivé, la réussite est proche !",
        "Soyez fier de votre parcours !",
        "Chaque effort vous rapproche de votre but !",
        "Vous êtes incroyable, continuez ainsi !"
    ]

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

        if nb_games_played % config.EPSILON_UPDATE_PARTIE == 0: 
            update_epsilon()
        if random.random() < 0.05:
            print(random.choice(phrases_of_encouragement))

    print(f"{nb_games_played}/{config.MAX_GAMES} parties jouées")

    if nb_games_played == config.MAX_GAMES :
        print("Entrainement terminé !")

if __name__ == "__main__":

    with app.app_context():
        try  :
            training()
        except ValueError as e:
            print("error : " + str(e))
            

    #si nb_games_played = MAX_GAMES -> lancer l'évaluation contre elle même et contre random



