from ChessGame import ChessGame
from Bots import *

game = ChessGame()

while not game.get_winner():
    bot = Kevin()
    move_list = game.get_all_legal_moves()
    bot_move = bot.pick_move(move_list)
    game.move(str(bot_move))
    print_all(game)
print("Result: ", game.get_winner())