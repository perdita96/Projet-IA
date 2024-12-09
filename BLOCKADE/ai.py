import random
from .app_models.models import *
import config


def possible_move(game, player_id):
    """
    Fonction qui renvoie les mouvements possibles pour l'IA.
    
    Pré-conditions :
        - game : instance de la classe Game représentant l'état actuel de la partie.
        - player_id : identifiant du joueur qui effectue le mouvement, doit être présent dans la partie.(IA)
    
    Post-conditions : 
        Retourne une liste des mouvements valides (Up, Down, Left, Right) que le joueur peut effectuer.
    """
    board_state = game.board_state
    size = game.size
    if player_id == game.player_1_id : 
        current_player = "1"
        current_pos = game.pos_player_1
    else :
        current_player = "2"
        current_pos = game.pos_player_2

    x, y = map(int, current_pos.split(","))
    possible_move = []
    for move in ['Up', 'Down', 'Left', 'Right']:
        match move:
            case "Up":
                new_x, new_y = x - 1, y
            case "Down":
                new_x, new_y = x + 1, y
            case "Left":
               new_x, new_y = x, y - 1
            case "Right":
                new_x, new_y = x, y + 1
        if 0 <= new_x < size and 0 <= new_y < size: 
            target_square = board_state[new_x * size + new_y]
            if target_square == "0" or target_square == current_player:
                possible_move.append(move.lower())
    return possible_move

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
    current_state = state(game)
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
    return "Arrow" + move.capitalize()

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

def state(game):
    """
    Génère un entier représentant l'état actuel d'un jeu basé sur les informations des joueurs et l'état du plateau.

    Pré-conditions :
        - game : instance de la classe Game représentant l'état actuel de la partie.

    Post-conditions : 
        Retourne un entier représentant l'état du jeu, obtenu par la conversion.
    """
    current_player = 1 if game.turn_player_1 else 2
    pos_player_1 = game.pos_player_1.replace(',', '')
    pos_player_2 = game.pos_player_2.replace(',', '')

    return f"{current_player}{pos_player_1}{pos_player_2}{game.board_state}"


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
    
    max_current_q_value = max(current_q_table_entry.up, current_q_table_entry.down, 
                              current_q_table_entry.left, current_q_table_entry.right)

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


def end_game(game, player_id):
    """
    Gère la fin du jeu. En mettant à jour la Q-table pour le dernier mouvement.
        Pré-conditions :
        - game : instance de la classe Game représentant l'état actuel de la partie.
        - player_id : Le numéro du joueur de IA.
    """
    previous_state_move = db.session.query(PreviousStateAction).filter_by(game_id=game.game_id, player_id=player_id).first()
    current_state = state(game)
    update_q_table(previous_state_move, current_state)
    db.session.commit()

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