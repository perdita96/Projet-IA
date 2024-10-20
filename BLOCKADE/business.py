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
            current_player_pos = game.pos_player_1
        elif int(player) == player_2.player_id:
            current_player = "2"
            current_player_pos = game.pos_player_2
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
                target_case = board_state[new_x * size + new_y]
                if (target_case == "0" or target_case == current_player):
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
                else:
                    raise ValueError("Mouvement non autorisé")
            else:
                raise ValueError("Mouvement en dehors du plateau")
        else:
            raise ValueError("Ce n'est pas au tour du joueur")
    else:
        raise ValueError("Direction non valide")


def is_within_board(x, y , board_size) :
    return (0 <= x < board_size) and (0 <= y < board_size)