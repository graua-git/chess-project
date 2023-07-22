# Console UI
# Configure profiles and how many games to play using the constants on the top

from Chess.ChessGame import *
from Chess.Profile import *

WHITE = Player('W')
BLACK = Kevin('B')
NUM_GAMES = 1

def play_games(white: Profile, black: Profile, num_games: int) -> dict:
    data = {'W': 0, 'B': 0, 'D': 0}
    for i in range(num_games):
        winner = play_game(white, black)
        data[winner] += 1
    return data

def play_game(white: Profile, black: Profile) -> str:
    game = ChessGame()
    players = {'W': white, 'B': black}
    while not game.get_winner():
        curr_player = players[game.get_turn()]
        if isinstance(curr_player, Player):
            game.print_all()
        move = curr_player.pick_move(game)
        game.move(str(move))
    game.print_all()
    print("Result: ", game.get_winner())
    return game.get_winner()

if __name__ == '__main__':
    print(str(play_games(WHITE, BLACK, NUM_GAMES)))
