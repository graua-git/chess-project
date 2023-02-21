from tkinter import *
from Game.Coord import *

ROOT = Tk()

def init_main_page():
    global ROOT
    for x in range(8):
        for y in range(8):
            coord = Coord(x, y)
            square_color = 'dark' if (x + y) % 2 == 0 else 'light'
            image = PhotoImage(file='images/B_Bishop.png')
            square = Button(ROOT, text=str(coord.x()) + ', ' + str(coord.y()), image = image, height = 6, width = 13, 
                            command=lambda coord=coord: print(coord))
            square.grid(row=8-y, column=x, sticky='nsew')

if __name__ == '__main__':
    
    ROOT.title("Chess")
    ROOT.wm_geometry("800x800")
    test()
    ROOT.mainloop()