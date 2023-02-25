from ChessGame import *
from tkinter import *
from tkinter.ttk import *

global root
global curr_game
global square1

def get_file_name(x: int, y: int):
    board = curr_game.get_current_board()
    piece = board[x][y]
    if not piece:
        return "Game/images/blank.png"
    else:
        return "Game/images/" + piece.get_team() + "_" + piece.get_name() + ".png"

def buttonclick(x, y):
    global curr_game, square1
    if square1:
        square2 = Coord(x, y)
        if square1 == square2:
            return 
        try:
            move = Move(curr_game.get_current_board(), curr_game.get_turn(), curr_game.get_turn_number(), square1, square2)
            curr_game.move(move)
            print(move)
        except InvalidMoveError:
            pass
        square1 = None
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
            if "blank" in file:
                photo = photo.subsample(4, 4)
            square_ref[x][y] = Button(root, image=photo, command=lambda x=x, y=y: buttonclick(x, y))
            square_ref[x][y].image = photo
            square_ref[x][y].grid(row=7-y, column=x)

if __name__ == '__main__':
    root = Tk()
    curr_game = ChessGame()
    square1 = None
    init_mainpage()
    mainloop()