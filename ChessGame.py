from Board import *
from MoveLog import *

class ChessGame:
    def __init__(self, starting_moves: str = None):
        """
        starting_moves: MoveLog to set the board to a certain position, optional
        """
        self._board = Board()
        self._move_log = MoveLog(starting_moves)
        self._turn = 'W'
        self.winner = None

    def __repr__(self):
        return str(self._board)
    
    def move(self, move):
        """
        Makes move, updating board and move log
        """
        # Verify move
        turn = self._board.turn()
        try:
            curr_move = Move(self._board, turn, move)
        except InvalidMoveError:
            return

        self._move_log.append(curr_move)
        self._board = curr_move.board_state()
        self._board.switch_turns()

if __name__ == '__main__':
    game = ChessGame()
    game.move('e4')
    game.move('e5')
    game.move('Nc3')
    game.move('Nc6')
    game.move('Bc4')
    game.move('Bc5')
    print(game)