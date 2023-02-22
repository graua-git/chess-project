from ChessGame import ChessGame
from Bots import *
import time

results = {'W': 0, 'B': 0, 'D': 0}

for i in range(100):
    white = Kevin('W')
    black = Kevin('B')
    
    game = ChessGame()
    bots = {'W': white, 'B': black}

    while not game.get_winner():
        move_list = game.get_all_legal_moves()
        bot = bots[game.get_turn()]
        bot_move = bot.pick_move(game)
        game.move(str(bot_move))
        print_all(game)

    winner = game.get_winner()
    results[winner] += 1

print(results)