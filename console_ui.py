from ChessGame import ChessGame

if __name__ == '__main__':
    game = ChessGame()
    new_game = ''
    new_game = input('New game (Y / N): ')
    while new_game != 'Y'.upper() and new_game != 'N'.upper():
        print('Unexpected Answer, please type Y for new game, or N to set a starting position')
        new_game = input('New game (Y / N): ')
    if new_game == 'Y':