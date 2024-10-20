import random


def get_move(game, player_id):
    """
    Pré-conditions :
        L'id du joueur qui fait le mouvement doit être l'id d'un joueur présent dans la game
    Post-conditions : 
        Retourne un mouvement valide sur la plateau du jeu
    """
    directions = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight']

    move =  random.choice(directions)
    while(not is_move_possible(game,player_id,move)) :
         move =  random.choice(directions)
    return move



def is_move_possible(game, player_id, move) : 
    """
    Pré-conditions :
        L'id du joueur qui fait le mouvement doit être l'id d'un joueur présent dans la game
        Le mouvement doit être [ArrowUp,ArrowDown,ArrowLeft,ArrowRight]
    Post-conditions : 
        Retourne true ou false en fonction de si le mouvement est valide
    """
    board_state = game.board_state
    size = game.size
    is_possible = True

    if player_id == game.player_1_id : 
        current_player = "1"
        current_pos = game.pos_player_1
    else :
        current_player = "2"
        current_pos = game.pos_player_2

    x, y = map(int, current_pos.split(","))

    if move == "ArrowUp":
        new_x, new_y = x - 1, y
    elif move == "ArrowDown":
        new_x, new_y = x + 1, y
    elif move == "ArrowLeft":
        new_x, new_y = x, y - 1
    elif move == "ArrowRight":
        new_x, new_y = x, y + 1

    is_possible =  (0 <= new_x < size) and (0 <= new_y < size)

    if is_possible : 
        target_square = board_state[new_x * size + new_y]
        is_possible = (target_square == "0" or target_square == current_player)
        
    return is_possible    