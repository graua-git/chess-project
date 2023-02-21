from ChessGame import *
import random

class Kevin():
    def pick_move(self, move_list: list) -> Move:
        """
        Takes list of all legal moves, picks one at random
        """
        return random.choice(move_list)