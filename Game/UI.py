from ChessGame import *
from Bots import Kevin

game = ChessGame()

bot = {
    'name': Kevin(),
    'team': 'B'
}

while not game.get_winner():
    if game.get_turn() == bot['team']:
        print_all(game)
        move_list = game.get_all_legal_moves()
        bot_move = bot['name'].pick_move(move_list)
        game.move(str(bot_move))
    
    else:
        print_all(game)
        move = input("Your move: ")
        try:
            game.move(move)
        except InvalidMoveError:
            continue

print_all(game)
print("Result: ", game.get_winner())