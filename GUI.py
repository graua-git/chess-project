from Chess.ChessGame import *
from tkinter import *
from tkinter.ttk import *
from Bots import *

global root
global curr_game
global turn, player_team

global square_ref
global square1
global bot

def get_file_name(x: int, y: int):
    board = curr_game.get_current_board()
    piece = board[x][y]
    suffix = '_dark.png' if (x + y) % 2 == 0 else '_light.png'
    if not piece:
        return "images/empty" + suffix
    else:
        return "images/" + piece.get_team().lower() + "_" + piece.get_name().lower() + suffix

def buttonclick(x, y):
    global curr_game, turn, square1, bot
    if turn != player_team:
        return
    if square1:
        square2 = Coord(x, y)
        if square1 == square2:
            return 
        try:
            move = Move(curr_game.get_current_board(), curr_game.get_turn(), curr_game.get_turn_number(), square1, square2)
        except InvalidMoveError:
            square1, square2 = Coord(x, y), None
            return
        
        
        curr_game.move(move)
        turn = 'W' if turn == 'B' else 'B'
        square1, square2 = None, None
        print(move)

        init_mainpage()
        bot_move = bot.pick_move(curr_game)
        curr_game.move(bot_move)
        turn = 'W' if turn == 'B' else 'B'
        init_mainpage()
    else:
        square1 = Coord(x, y)
        return

def init_mainpage():
    global root, curr_game
    square_ref = [[None for x in range(8)] for x in range(8)]
    photo = PhotoImage()
    for x in range(8):
        for y in range(8):
            file = get_file_name(x, y)
            photo = PhotoImage(file=file)
            square_ref[x][y] = Button(root, image=photo, command=lambda x=x, y=y: buttonclick(x, y))
            square_ref[x][y].image = photo
            square_ref[x][y].grid(row=7-y, column=x)

if __name__ == '__main__':
    root = Tk()
    curr_game = ChessGame()
    square1 = None
    turn = 'W'
    player_team = 'W'
    bot = Kevin('B')
    init_mainpage()
    mainloop()