from Game.ChessGame import *
from Game.Kevin import Kevin

game = ChessGame()

while True:
    move = input("Your move: ")
    try:
        game.move(move)
    except InvalidMoveError:
        continue

    bot = Kevin()
    move_list = game.get_all_legal_moves()
    bot_move = bot.pick_move(move_list)
    game.move(str(bot_move))

    print_all(game)
