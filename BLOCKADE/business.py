def move(game, player, direction):
    player_1 = game.player_1
    player_2 = game.player_2
    board_state = game.board_state
    size = game.size

    if player == player_1.player_id:
        current_player = "1"
        current_player_pos = game.pos_player_1
    elif player == player_2.player_id:
        current_player = "2"
        current_player_pos = game.pos_player_2

    if (game.turn_player_1 and current_player == "1") or (not game.turn_player_1 and current_player == "2"):
        x, y = map(int, current_player_pos.split(","))

        if direction == "up":
            new_x, new_y = x - 1, y
        elif direction == "down":
            new_x, new_y = x + 1, y
        elif direction == "left":
            new_x, new_y = x, y - 1
        elif direction == "right":
            new_x, new_y = x, y + 1
        else:
            raise ValueError("Direction non valide")

        if (0 <= new_x < size) and (0 <= new_y < size):
            target_case = board_state[new_x * size + new_y]

            if (target_case == "0" or target_case == current_player):
                if current_player == 1:
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