import random

def possible_move(game, player_id):
    """
    Fonction qui revoir les mouvements possible pour l'IA
    Pré-conditions :
        - game est la game en cour
        - L'id du joueur qui fait le mouvement doit être l'id d'un joueur présent dans la game
    Post-conditions : 
        Retourne la liste des mouvements valides
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
    for move in ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight']:
        match move:
            case "ArrowUp":
                new_x, new_y = x - 1, y
            case "ArrowDown":
                new_x, new_y = x + 1, y
            case "ArrowLeft":
               new_x, new_y = x, y - 1
            case "ArrowRight":
                new_x, new_y = x, y + 1
        if((0 <= new_x < size) and (0 <= new_y < size)): 
            target_square = board_state[new_x * size + new_y]
            if(target_square == "0" or target_square == current_player):
                possible_move.append(move)
    return possible_move

def get_move(game, player_id):
    """
    Fonction qui revoir le mouvement choisit par l'IA
    Pré-conditions :
        - game est la game en cour
        - L'id du joueur qui fait le mouvement doit être l'id d'un joueur présent dans la game
    Post-conditions : 
        Retourne un mouvement valide sur la plateau du jeu
    """

    directions = possible_move(game, player_id)
    return random.choice(directions)