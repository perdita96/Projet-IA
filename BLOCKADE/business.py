from math import sqrt


def move(game, player, direction):
    """
    Pré-conditions :
        game est un objet Game valide
        player est un ID de joueur 
        direction est une chaîne
        Le jeu n'est pas déjà terminé (c'est-à-dire que game.winner_player_1 est None)
    Post-conditions :
        Si le déplacement est valide, la fonction met à jour l'état du jeu en conséquence :
            Met à jour la position du joueur (game.pos_player_1 ou game.pos_player_2)
            Met à jour l'état du plateau (game.board_state)
            Met à jour l'indicateur game.turn_player_1
            Si le jeu est terminé, définit game.winner_player_1
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
        current_player_pos = game.pos_player_1
    elif int(player) == player_2.player_id:
        current_player = "2"
        current_player_pos = game.pos_player_2
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
    if (target_case != "0" and target_case != current_player):
        raise ValueError("Mouvement non autorisé")
    
    if current_player == "1":
        game.pos_player_1 = f"{new_x},{new_y}"
    else:
        game.pos_player_2 = f"{new_x},{new_y}"

    board_state = list(board_state)
    board_state[new_x * size + new_y] = current_player
    game.board_state = "".join(board_state)
    game.turn_player_1 = not game.turn_player_1

    if "0" not in board_state:
        game.winner_player_1 = board_state.count("1") > size ** 2 // 2
    
    return game


def is_within_board(x, y, board_size) :
    return (0 <= x < board_size) and (0 <= y < board_size)

def is_move_valid(player_number, case_state) : 
    return player_number == case_state

def box_is_accessible(board_state, i_case, player_number) : 
    return player_number in [0, board_state[i_case]]

def reachable_cases(opponent_number, opponent_pos, board_state) : 
    board_size = len(board_state)
    side_size = sqrt(board_size)

    reachable = [False] * board_size

    x,y = map(int, opponent_pos.split(","))
    queue = [board_state[x * board_size + y]]

    while queue : #vérif la condition?
        todo = queue.popleft()

        neighbor_case = [todo - side_size, todo + side_size, todo + 1, todo - 1]

        i_neighbor = 0
        while neighbor_case[i_neighbor] < 4 :
            i_case = neighbor_case[i_neighbor]
            if 0 <= i_case < board_size and not reachable[i_case] and box_is_accessible(board_state, i_case, opponent_number) : 
                reachable[i_case] = True
                queue.append(i_case)

            i_case += 1

    return reachable
