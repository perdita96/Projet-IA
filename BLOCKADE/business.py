from math import sqrt


def move(game, player, direction):
    """
    Fonction qui bouge le joueur sur le plateau de jeu.

    Pré-conditions :
        game est un objet Game valide
        player est un ID de joueur 
        direction est une chaîne
        Le jeu n'est pas déjà terminé (c'est-à-dire que game.winner est falsy)
    Post-conditions :
        Si le déplacement est valide, la fonction met à jour l'état du jeu en conséquence :
            Met à jour la position du joueur (game.pos_player_1 ou game.pos_player_2)
            Met à jour l'état du plateau (game.board_state)
            Met à jour l'indicateur game.turn_player_1
            Si le jeu est terminé, définit game.winner
        Lance un valueError si une valeur n'est pas valide ou un mouvement impossible
    """
    player_1 = game.player_1
    player_2 = game.player_2
    board_state = game.board_state
    size = game.size

    directions = ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight']
    if direction not in directions:
        raise ValueError("Direction non valide")
    
    if int(player) == player_1.player_id:
        current_player = "1"
        opponent_player = "2"
        current_player_pos = game.pos_player_1
        opponent_player_pos = game.pos_player_2
    elif int(player) == player_2.player_id:
        current_player = "2"
        opponent_player = "1"
        current_player_pos = game.pos_player_2
        opponent_player_pos = game.pos_player_1
    else:
        raise ValueError("Player is not in the game")

    if (not game.turn_player_1 and current_player == "1") or (game.turn_player_1 and current_player == "2"):
        raise ValueError("Ce n'est pas au tour du joueur")
    
    x, y = map(int, current_player_pos.split(","))
    match direction:
        case "ArrowUp":
            new_x, new_y = x - 1, y
        case "ArrowDown":
            new_x, new_y = x + 1, y
        case "ArrowLeft":
            new_x, new_y = x, y - 1
        case "ArrowRight":
            new_x, new_y = x, y + 1
        case _:
            raise ValueError("Direction non valide")
                
    if (not is_within_board(new_x, new_y , size)):
        raise ValueError("Mouvement en dehors du plateau")
    
    target_case = board_state[new_x * size + new_y]
    if (not is_move_valid(target_case, current_player)): 
        raise ValueError("Mouvement non autorisé")
    
    if current_player == "1":
        game.pos_player_1 = f"{new_x},{new_y}"
    else:
        game.pos_player_2 = f"{new_x},{new_y}"

    board_state = list(board_state)
    board_state[new_x * size + new_y] = current_player

    board_state = update_enclosure(opponent_player, opponent_player_pos, board_state)
                                    
    game.board_state = "".join(board_state)
    game.turn_player_1 = not game.turn_player_1

    if "0" not in board_state:
        game.winner = 1 if board_state.count("1") > size ** 2 // 2 else 2
    
    return game


def is_within_board(x, y, side_size) : 
    """
    Fonction qui vérifie si la case est dans le plateau

    Préconditions:
    - x et y doivent être des entiers.
    - side_size doit être un entier positif.

    Postconditions:
    - Retourne True si (x, y) est dans les limites du plateau, sinon False.
    """
    return (0 <= x < side_size) and (0 <= y < side_size)


def is_move_valid(target_case, player_number) : 
    """
    Fonction qui vérifie si le mouvement est valide
<<<<<<< HEAD
    
=======

>>>>>>> 7d28c24d93e3920c70d96110f9248c985d280eeb
    Préconditions:
    - target_case doit être un caractère de la chaîne représentant l'état du jeu.
    - player_number est le numéro du joueur.

    Postconditions:
    - Retourne True si le mouvement est valide, c'est à dire que target_case n'est pas occupé par l'adversaire, sinon False.
    """
    return target_case == "0" or target_case == player_number

def reachable_cases(opponent_number, opponent_pos, board_state) : 
    """
    Fonction qui trouve les cases accessibles ou non par un joueur

    Préconditions:
    - opponent_number est le numéro du joueur adverse.
    - opponent_pos doit être une chaîne de caractères au format "x,y" représentant la position actuelle du joueur adverse.
    - board_state doit être une chaîne de caractères représentant l'état du jeu.

    Postconditions:
    - Retourne une liste de booléens indiquant si chaque case est accessible ou non par le joueur adverse.
    """

    board_size = len(board_state)
    side_size = int(sqrt(board_size))

    reachable = [False] * board_size

    x,y = map(int, opponent_pos.split(","))

    queue = [(x, y)]

    while queue : 
        x_case, y_case = queue.pop(0)

        neighbor_cases = [(x_case - 1, y_case), (x_case , y_case-1), (x_case + 1, y_case), (x_case, y_case + 1) ]

        for x_neighbor, y_neighbor in neighbor_cases :
            i_case = x_neighbor * side_size + y_neighbor

            if is_within_board(x_neighbor, y_neighbor, side_size) and not reachable[i_case] and is_move_valid(board_state[i_case], opponent_number) : 
                reachable[i_case] = True
                if((x_neighbor, y_neighbor) not in queue):
                    queue.append((x_neighbor, y_neighbor)) 


    return reachable

def update_enclosure(opponent_number, opponent_pos, board_state) :
    """
    Fonction qui met a jour l'état du plateau avec les enclos (cases inaccessibles par l'adversaire)

    Préconditions:
    - opponent_number est le numéro du joueur adverse.
    - opponent_pos doit être une chaîne de caractères au format "x,y" représentant la position actuelle du joueur adverse.
    - board_state doit être une chaîne de caractères représentant l'état du jeu.

    Postconditions:
    - Retourne l'état du plateau mis à jour.
    """
    reachable = reachable_cases(opponent_number, opponent_pos, board_state)

    if opponent_number == "1" : 
        current_player_number = "2"
    else :
        current_player_number = "1"
        
    board_size = len(board_state)

    for i_case in range(board_size) :
        if(not reachable[i_case]) :
            board_state[i_case] = current_player_number
            
    return board_state