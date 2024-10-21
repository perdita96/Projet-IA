from math import sqrt


def move(game, player, direction):
    """
    Pré-conditions
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
    if direction in directions:
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

        if (game.turn_player_1 and current_player == "1") or (not game.turn_player_1 and current_player == "2"):
            x, y = map(int, current_player_pos.split(","))
            if direction == "ArrowUp":
                new_x, new_y = x - 1, y
            elif direction == "ArrowDown":
                new_x, new_y = x + 1, y
            elif direction == "ArrowLeft":
                new_x, new_y = x, y - 1
            elif direction == "ArrowRight":
                new_x, new_y = x, y + 1
            else:
                raise ValueError("Direction non valide")
            if (is_within_board(new_x, new_y , size)):
                target_square = board_state[new_x * size + new_y]
                if (is_move_valid(target_square, current_player)): 
                    if current_player == "1":
                        game.pos_player_1 = f"{new_x},{new_y}"
                    else:
                        game.pos_player_2 = f"{new_x},{new_y}"

                    board_state = list(board_state)
                    board_state[new_x * size + new_y] = current_player

                    board_state = board_state_with_pen(opponent_player, opponent_player_pos, board_state)
                    
                    
                    game.board_state = "".join(board_state)
                    game.turn_player_1 = not game.turn_player_1
                    if "0" not in board_state:
                        game.winner_player_1 = board_state.count("1") > size ** 2 // 2
                    return game
                else:
                    raise ValueError("Mouvement non autorisé")
            else:
                raise ValueError("Mouvement en dehors du plateau")
        else:
            raise ValueError("Ce n'est pas au tour du joueur")
    else:
        raise ValueError("Direction non valide")


def is_within_board(x, y, side_size) : 
    """
    Pré-conditions
        x et y sont des entiers qui représentent des coordonnées sur le plateau
        side_size est un entier qui représente la longueur des côtés du plateau
    Post-conditions :
        Si les coordonnées sont dans le plateau renvoie true sinon false
    """
    return (0 <= x < side_size) and (0 <= y < side_size)


def is_move_valid(target_square, player_number) :
    """
    Pré-conditions
       player_number est un entier représentant le numéro du joueur (1 ou 2)
       target_square est un entier représentant le numéro de la case que le joueur veut accéder :
            - (0 -> libre, 1 -> appartient au joueur 1, 2 -> appartient au joueur 2)
    Post-conditions :
        Si la case est libre ou appartient déjà au joueur alors renvoie true sinon false
    """ 
    return target_square == "0" or target_square == player_number

def reachable_squares(opponent_number, opponent_pos, board_state) : 
    """
    Pré-conditions :
        opponent_number est entier représentant le numéro (1 ou 2) de l'advairsaire du joueur courant
        opponent_pos est une chaine de caractères représentant les coordonnées sur le plateau de l'adversaire : 
            - le format doit être "x,y"
        board_state est une chaine de caractères représentant l'état actuel du plateau :
            - la case est (0 -> libre, 1 -> appartient au joueur 1, 2 -> appartient au joueur 2)
    Post-conditions :
        renvoie un tableau de la taille du plateau de jeu indiquant pour chacune des cases True si elles sont atteignables par l'adversaire ou False si pas
    """ 

    board_size = len(board_state)
    side_size = int(sqrt(board_size))

    reachable = [False] * board_size

    x,y = map(int, opponent_pos.split(","))

    queue = [(x, y)]

    while queue : 
        x_square, y_square = queue.pop(0)

        neighbor_squares = [(x_square - 1, y_square), (x_square , y_square-1), (x_square + 1, y_square), (x_square, y_square + 1) ]

        i_neighbor = 0
        while(i_neighbor < 4) :
            x_neighbor, y_neighbor = neighbor_squares[i_neighbor]
            i_square = x_neighbor * side_size + y_neighbor
            
            if is_within_board(x_neighbor, y_neighbor, side_size) and not reachable[i_square] and is_move_valid(board_state[i_square], opponent_number) : 
                reachable[i_square] = True
                queue.append((x_neighbor, y_neighbor))

            i_neighbor +=1

    return reachable

def board_state_with_pen(opponent_number, opponent_pos, board_state) :
    """
    Pré-conditions :
        opponent_number est entier représentant le numéro (1 ou 2) de l'advairsaire du joueur courant
        opponent_pos est une chaine de caractères représentant les coordonnées sur le plateau de l'adversaire : 
            - le format doit être "x,y"
        board_state est une chaine de caractères représentant l'état actuel du plateau :
            - la case est (0 -> libre, 1 -> appartient au joueur 1, 2 -> appartient au joueur 2)
    Post-conditions :
        Met à jour l'état du plateau avec le traitement des enclos du joueur courant
    """ 
    reachable = reachable_squares(opponent_number, opponent_pos, board_state)

    if opponent_number == "1" : 
        current_player_number = "2"
    else :
        current_player_number = "1"
        
    board_size = len(board_state)
    i_square = 0
    while i_square < board_size : 
        if(not reachable[i_square]) :
            board_state[i_square] = current_player_number
        i_square +=1

    return board_state

        

