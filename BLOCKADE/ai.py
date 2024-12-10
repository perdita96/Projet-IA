import random
from .app_models.models import *
import config
from .business import possible_move


def get_move(game, player_id):
    """
    Fonction qui renvoie le mouvement choisi par l'IA et met à jour les données d'apprentissage.
    
    Pré-conditions :
        - game : instance de la classe Game représentant l'état actuel de la partie.
        - player_id : identifiant du joueur qui effectue le mouvement, doit être présent dans la partie.(IA)
    
    Post-conditions : 
        Retourne un mouvement valide sur le plateau du jeu sous la forme d'une chaîne de caractères, par exemple "ArrowUp".
        Met à jour les données d'apprentissage, c'est a dire la Q-Table et previous_state_move dans la base de données

    """
    previous_state_move = db.session.query(PreviousStateAction).filter_by(game_id=game.game_id, player_id=player_id).first()
    current_player_number = "1" if player_id == game.player_1_id else "2"
    current_state = state(game,current_player_number)
    if previous_state_move:
        update_q_table(previous_state_move, current_state)
    else:
        previous_state_move = PreviousStateAction(
            game_id=game.game_id,
            player_id=player_id,
            previous_state=None,
            previous_action=None)
        db.session.add(previous_state_move)
    previous_state_move.previous_state = current_state
    if random.random() < config.EPS:
        move = explore(game, player_id)
    else:
        move = exploit(game, player_id, current_state)
    previous_state_move.previous_action = move
    db.session.commit()
    return move

def explore(game, player_id):
    """
    Fonction qui renvoie le mouvement choisi par l'IA lors de la phase d'exploration.
    
    Pré-conditions :
        - game : instance de la classe Game représentant l'état actuel de la partie.
        - player_id : identifiant du joueur qui effectue le mouvement, doit être présent dans la partie.(IA)
    
    Post-conditions : 
        Retourne un mouvement valide sur le plateau du jeu choisi aléatoirement parmi les mouvements possibles.
    """
    directions = possible_move(game, player_id)
    return random.choice(directions)

def exploit(game, player_id, current_state):
    """
    Fonction qui renvoie le mouvement choisi par l'IA lors de la phase d'exploitation.
    
    Pré-conditions :
        - game : instance de la classe Game représentant l'état actuel de la partie.
        - player_id : identifiant du joueur qui effectue le mouvement, doit être présent dans la partie.(IA)
        - current_state : l'état actuel du jeu sous forme d'entier.
    
    Post-conditions : 
        Retourne le meilleur mouvement possible basé sur la Q-table, ou un mouvement aléatoire si current_state n'est pas dans la base de données.
    """
    value_state = db.session.query(Qtable).get(current_state) 
    if value_state:
        best_action = None
        best_value = -float('inf')
        directions = possible_move(game, player_id)
        for direction in directions:
            value = getattr(value_state, direction)
            if (value > best_value):
                best_value = value
                best_action = direction
        return best_action
    else:
        return explore(game, player_id)

def state(game, current_player_number):
    """
    Génère un entier représentant l'état actuel d'un jeu basé sur les informations des joueurs et l'état du plateau.

    Pré-conditions :
        - game : instance de la classe Game représentant l'état actuel de la partie.
        - current_player_number : est le numéro du joueur qui modifie la q-table

    Post-conditions : 
        Retourne un entier représentant l'état du jeu, obtenu par la conversion.
    """
    pos_player_1 = game.pos_player_1.replace(',', '')
    pos_player_2 = game.pos_player_2.replace(',', '')

    return f"{current_player_number}{pos_player_1}{pos_player_2}{game.board_state}"


def update_q_table(previous_state_move, current_state):
    """
    Met à jour la Q-table en fonction de l'état précédent, de l'état actuel et de l'action effectuée.

    Pré-conditions :
        - previous_state_move : Instance de la classe PreviousStateAction représentant l'état précédent du joueur et l'action effectuée.
        - current_state : Entier représentant l'état actuel du jeu.
            Contient -> cur_player_nb, pos_player_1 (x,y), pos_player_2 (x,y), board_state

    Post-conditions :
        - Met à jour la Q-table avec la nouvelle valeur calculée pour l'action effectuée.
    """
    learning_rate = config.LEARNING_RATE 
    discount_factor = config.DISCOUNT_FACTOR 

    current_player_number = str(current_state[0])

    # On commence à 5 car il y a cur_player, pos_player_1 et pos_player_2 avant
    previous_boardstate = previous_state_move.previous_state[5:] 
    current_boardstate = current_state[5:]
    
    reward = calculate_reward(previous_boardstate, current_boardstate, current_player_number)  
    
    # Ajouter les états dans la Qtable s'ils n'existent pas
    if not db.session.query(Qtable).get(previous_state_move.previous_state):
        new_entry = Qtable(state=previous_state_move.previous_state)
        db.session.add(new_entry)
    if not db.session.query(Qtable).get(current_state):
        new_entry = Qtable(state=current_state)
        db.session.add(new_entry)
    
    action = previous_state_move.previous_action

    previous_q_table_entry = db.session.query(Qtable).get(previous_state_move.previous_state)
    previous_q_value = getattr(previous_q_table_entry, action)

    current_q_table_entry = db.session.query(Qtable).get(current_state)
    
    max_current_q_value = max(current_q_table_entry.ArrowUp, current_q_table_entry.ArrowDown, 
                              current_q_table_entry.ArrowLeft, current_q_table_entry.ArrowRight)

    new_q_value = previous_q_value + learning_rate * (reward + discount_factor * max_current_q_value - previous_q_value)

    setattr(previous_q_table_entry, action, new_q_value)
    db.session.commit()

def calculate_reward(previous_boardstate, current_boardstate, current_player_nb):
    """
    Calcule la récompense basée sur la transition d'état.

    Pré-conditions :
        previous_boardstate : L'état précédent du plateau (sous forme de chaîne).
        current_boardstate : L'état actuel du plateau (sous forme de chaîne).
        current_player_nb : Le numéro du joueur actuel (1 ou 2) sous forme de caractère.

    Post-conditions :
        int : Une récompense calculée, représentant la différence entre le nombre d'éléments pris et perdus.
    """
    nb_take = current_boardstate.count(current_player_nb) - previous_boardstate.count(current_player_nb)
    opponent_number = "1" if current_player_nb == "2" else "2"
    nb_lose = current_boardstate.count(opponent_number) - previous_boardstate.count(opponent_number)
    reward = nb_take - nb_lose
    if "0" not in current_boardstate:
        if nb_take > nb_lose:
            reward += current_boardstate.count(current_player_nb)
        elif nb_take < nb_lose:
            reward -= current_boardstate.count(opponent_number)
    return reward


def end_game_ai(game, player_id):
    """
    Gère la fin du jeu. En mettant à jour la Q-table pour le dernier mouvement.
        Pré-conditions :
        - game : instance de la classe Game représentant l'état actuel de la partie.
        - player_id : Le numéro du joueur de IA.
    """
    previous_state_move = db.session.query(PreviousStateAction).filter_by(game_id=game.game_id, player_id=player_id).first()
    current_player_number = 1 if player_id == game.player_1_id else 2
    current_state = state(game,current_player_number)
    update_q_table(previous_state_move, current_state)
    db.session.commit()

