# Console UI
# Configure profiles and how many games to play using the constants on the top

from Chess.ChessGame import *
from Chess.Profile import *


def play_games(white: Profile, black: Profile, num_games: int) -> dict:
    """
    Plays multiple games, returning the results in a dictionary
    W: # White wins
    B: # Black wins
    D: # Draws
    """
    data = {'W': 0, 'B': 0, 'D': 0}
    for i in range(num_games):
        winner = play_game(white, black)
        data[winner] += 1
    return data


def play_game(white: Profile, black: Profile) -> str:
    """
    Plays game, once concluded returns the result of the game
    W: White wins
    B: Black wins
    D: Draw
    """
    game = ChessGame()
    players = {'W': white, 'B': black}
    while not game.get_winner():
        # Get move based on player
        curr_player = players[game.get_turn()]
        if isinstance(curr_player, Player):
            game.print_all()
        move = curr_player.pick_move(game)
        # Commit move to the game
        game.move(str(move))
    game.print_all()
    print("Result: ", game.get_winner())
    return game.get_winner()


def choose_settings():
    """
    Prompts user input to select the players for white and black, as well as the number of games
    Returns the result as a tuple (white, black, num_games)
    """
    white_options = [None, Player('W'), Kevin('W'), Caleb('W'), Nick('W'), Luke('W')]
    black_options = [None, Player('B'), Kevin('B'), Caleb('B'), Nick('B'), Luke('B')]
    options_text = "Profile Options: \n \
                    1) Player: User controlled player through console inputs \n \
                    2) Kevin: Bot that picks a random move \n \
                    3) Caleb: Bot that takes pieces whenever possible \n \
                    4) Nick: Bot that positions its pieces \n \
                    5) Luke: Bot that evaluates different aspects of the board"
    print(options_text)
    white_index = -1
    while white_index > 5 or white_index < 0:
        try:
            white_index = int(input("SELECT WHITE PLAYER: "))
        except ValueError:
            pass
    black_index = -1
    while black_index > 5 or black_index < 0:
        try:
            black_index = int(input("SELECT BLACK PLAYER: "))
        except ValueError:
            pass
    num_games = int(input("SELECT NUMBER OF GAMES: "))
    return white_options[white_index], black_options[black_index], num_games


if __name__ == '__main__':
    white, black, num_games = choose_settings()
    print(str(play_games(white, black, num_games)))
