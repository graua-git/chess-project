from ChessGame import *
import random

class Bot:
    def __init__(self):
        pass

class Kevin(Bot):
    def __init__(self):
        Bot.__init__(self)

    def pick_move(self, move_list: list) -> Move:
        """
        Takes list of all legal moves, picks one to play
        Kevin picks one at random
        """
        return random.choice(move_list)
    
class Caleb(Bot):
    def __init__(self):
        Bot.__init__(self)
    
    def pick_move(self, move_list: list) -> Move:
        """
        Takes list of all legal moves, picks one to play
        Caleb is a quick, aggresive player, 
        """
        