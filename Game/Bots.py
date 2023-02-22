from ChessGame import *
import random
import copy

class Bot:
    def __init__(self, team):
        self.team = team

    def __repr__(self):
        return str(self.__name__)

class Kevin(Bot):
    def __init__(self, team: str):
        Bot.__init__(self, team)

    def pick_move(self, game: ChessGame) -> Move:
        """
        Takes list of all legal moves, picks one to play
        Kevin picks one at random
        """
        move_list = game.get_all_legal_moves()
        return random.choice(game.get_all_legal_moves())
    
class Caleb(Bot):
    def __init__(self, team: str):
        Bot.__init__(self, team)
    
    def pick_move(self, game: ChessGame) -> Move:
        """
        Takes list of all legal moves, picks one to play
        Caleb is a quick, aggresive player, taking whenever possible
        """
        move_list = game.get_all_legal_moves()
        taking_moves = [move for move in move_list if 'x' in str(move)]

        if len(taking_moves) == 0:
            return random.choice(move_list)
        return random.choice(taking_moves)
    
class Nick(Bot):
    def __init__(self, team: str):
        Bot.__init__(self, team)

    def pick_move(self, game: ChessGame) -> Move:
        """
        Takes a list of all legal moves, picks one to play
        Nick 
        """
        move_list = copy.deepcopy(game.get_all_legal_moves())
        move_list = []
        taking_moves = [move for move in move_list if 'x' in str(move)]

        if len(taking_moves) != 0:
            for move in taking_moves:
                move.board_state = copy.deepcopy(game.get_current_board())
