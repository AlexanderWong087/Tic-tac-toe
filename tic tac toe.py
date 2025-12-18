import sys

board = [['', '', ''],
         ['', '', ''],
         ['', '', '']]
current_player_global = 'X'

def make_move(player, cell):
    global board
    cell_coords = [(cell - 1) // 3, (cell - 1) % 3]
    x, y = cell_coords
    if cell < 1 or cell > 9:
        return ['0', 'Input out of range', player]
    if board[x][y] != '':
        return ['0', 'Input overwrites already filled in cell', player]
    board[x][y] = player
    return '1'

def check_win(board):
    winning_combinations = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
    ]
    for combination in winning_combinations:
        if combination[0] == combination[1] == combination[2] != '':
            return 'win'
    
    return 'draw' if all(cell != '' for row in board for cell in row) else 'continue'

def save(board, playerturn):
    with open('Game.txt', mode='w') as file:
        for row in board:
            file.write(','.join(cell if cell else ' ' for cell in row) + '\n')
        file.write(playerturn + '\n')
def load():
    try:
        with open('Game.txt', mode='r') as file:
            lines = file.readlines()
            if len(lines) < 4:  # Ensure there are enough lines for the board and player turn
                raise ValueError("Corrupted save file: Not enough data.")
            board = [line.strip().split(',') for line in lines[:-1]]
            playerturn = lines[-1].strip()
            if playerturn not in ['X', 'O']:  # Validate player turn
                raise ValueError("Corrupted save file: Invalid player turn.")
            return board, playerturn
    except FileNotFoundError:
        print('You did not save a game, moved it, or changed the name. Please try again.')
        sys.exit()
    except ValueError as e:
        print(e)
        print('The save file is corrupted. Please start a new game.')
        sys.exit()
def request_load():
    load_input = input('Would you like to load a prior game? (Yes/No): ')
    if load_input.lower() == 'yes':
        try:
            return load()
        except FileNotFoundError:
            print('You did not save a game, moved it, or changed the name. Please try again.')
            sys.exit()
    return board, 'X'  # Default to player X if not loading

def request_input(player):
    print('Current board:')
    for row in board:
        print(' | '.join(cell if cell != '' else ' ' for cell in row))
        print('-' * 9)
    fill_cell = input(f'Player {player}, please choose a cell from 1-9 to fill: ')
    output = make_move(player, int(fill_cell))
    return output

def main():
    global current_player_global
    board, current_player_global = request_load()
    
    while True:
        turn_info = request_input(current_player_global)
        if turn_info[0] == '1':
            current_player_global = 'O' if current_player_global == 'X' else 'X'
        else:
            print(turn_info[1])
            continue
        
        result = check_win(board)
        if result == 'win':
            for row in board:
                print(' | '.join(cell if cell != '' else ' ' for cell in row))
                print('-' * 9)
            if current_player_global=='O':
                print('Player X has won!')
            else:
                print('Player O has won!')
            break
        elif result == 'draw':
            for row in board:
                print(' | '.join(cell if cell != '' else ' ' for cell in row))
                print('-' * 9)
            print('The game is a draw!')
            break

        # Request to save the game after each turn
        save_request = input('Would you like to save the game? (Yes/No): ')
        if save_request.lower() == 'yes':
            save(board, current_player_global)
            print('Game saved successfully!')

if __name__ == "__main__":
    main()
