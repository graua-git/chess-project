from Move import *
from Board import *

class MoveLog:
    def __init__(self, log: str = None):
        """
        log: str representing list of moves to set position, optional
        """
        self._log = []
        if log:
            self._set_log(log)
    
    def __repr__(self):
        return self._log
    
    def _set_log(log: str) -> list[Move]:
        """
        Converts string move log into list
        """
        nums = '0123456789'
        board = Board()
        
        # Split string to get move notations
        move_list = log.split('. ')
        move_list.remove('1')
        string_move_list = ''
        for i in range(len(move_list)):
            string_move_list += move_list[i] + ' '
        move_list = string_move_list.split(' ')
        # Filter out empty strings
        move_list = [move for move in move_list if len(move) > 1]
        # Filter out turn number notation
        move_list = [move for move in move_list if move[0] not in nums]

        for move in move_list:
            try:
                curr = Move(board, move)
                board = curr.board_state()
            except InvalidMoveError:
                return
        
    def append(self, move: Move):
        """
        Appends move to move log
        """
        self._log.append(Move)