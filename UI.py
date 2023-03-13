from Chess.ChessGame import *
from Bots import *

game = ChessGame()

bot = Flau('B')

while not game.get_winner():
    if game.get_turn() == bot.team:
        game.print_all()
        move_list = game.get_all_legal_moves()
        bot_move = bot.pick_move(game)
        game.move(str(bot_move))
    
    else:
        game.print_all()
        move = input("Your move: ")
        try:
            game.move(move)
        except InvalidMoveError:
            continue

game.print_all()
print("Result: ", game.get_winner())