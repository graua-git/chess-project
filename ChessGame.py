from Board import *
from MoveLog import *

class ChessGame:
    def __init__(self, starting_moves: str = None):
        """
        starting_moves: MoveLog to set the board to a certain position, optional
        """
        self._board = Board()
        self._move_log = MoveLog(starting_moves)
        self.winner = None

    def __repr__(self):
        return str(self._board)
    
    def move(self, move):
        """
        Makes move, updating board and move log
        """
        # Verify move
        curr_move = Move(self._board.board_state(), move)

        # Move pieces

        
        self._move_log.append(curr_move)
    

if __name__ == '__main__':
    game = ChessGame()
    m = (Coord(0, 7), Coord(4, 3))
    game.move(m)