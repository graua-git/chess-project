from ChessGame import *
from tkinter import *
from tkinter.ttk import *

def get_file_name(game: ChessGame, x: int, y: int):
    board = game.get_current_board()
    piece = board[x][y]
    if not piece:
        return "Game/images/blank.png"
    else:
        return "Game/images/" + piece.get_team() + "_" + piece.get_name() + ".png"

def buttonclick(root, game, x, y):
    print(x, y)
    game.move('e4')
    init_mainpage(root, game)

def init_mainpage(root: Tk, game: ChessGame):
    square_ref = [[None for x in range(8)] for x in range(8)]
    photo = PhotoImage()
    for x in range(8):
        for y in range(8):
            file = get_file_name(game, x, y)
            photo = PhotoImage(file=file)
            if "blank" in file:
                photo = photo.subsample(4, 4)
            square_ref[x][y] = Button(root, image=photo, command=lambda x=x, y=y: buttonclick(root, game, x, y))
            square_ref[x][y].image = photo
            square_ref[x][y].grid(row=7-y, column=x)

if __name__ == '__main__':
    root = Tk()
    game = ChessGame()
    init_mainpage(root, game)
    mainloop()