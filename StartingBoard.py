# Class to create a 2D list to represent a chess board with pieces in their starting squares.

from Piece import Piece
from Coord import Coord

class StartingBoard:
    def __init__(self):
        self.board = self._init_new_board()

    def _init_new_board(self) -> None:
        """
        Creates a 2D array to represent the chess board in the starting position
        """
        # Create Rows
        board = [[None for x in range(8)] for x in range(8)]

        # Add Pawns
        for square in range(8):
            board[square][1] = Piece('Pawn', 'White', 1, Coord(square, 1))
            board[square][6] = Piece('Pawn', 'Black', 1, Coord(square, 6))

        # Add Knights
        board[1][0] = Piece('Knight', 'White', 3, Coord(1, 0))
        board[6][0] = Piece('Knight', 'White', 3, Coord(6, 0))
        board[1][7] = Piece('Knight', 'Black', 3, Coord(1, 7))
        board[6][7] = Piece('Knight', 'Black', 3, Coord(6, 7))
        
        # Add Bishops
        board[2][0] = Piece('Bishop', 'White', 3, Coord(2, 0))
        board[5][0] = Piece('Bishop', 'White', 3, Coord(5, 0))
        board[2][7] = Piece('Bishop', 'Black', 3, Coord(2, 7))
        board[5][7] = Piece('Bishop', 'Black', 3, Coord(5, 7))

        # Add Rooks
        board[0][0] = Piece('Rook', 'White', 5, Coord(0, 0))
        board[7][0] = Piece('Rook', 'White', 5, Coord(7, 0))
        board[0][7] = Piece('Rook', 'Black', 5, Coord(0, 7))
        board[7][7] = Piece('Rook', 'Black', 5, Coord(7, 7))

        # Add Queens
        board[3][0] = Piece('Queen', 'White', 9, Coord(3, 0))
        board[3][7] = Piece('Queen', 'Black', 9, Coord(3, 7))

        # Add Kings
        board[4][0] = Piece('King', 'White', 500, Coord(4, 0))
        board[4][7] = Piece('King', 'Black', 500, Coord(4, 7))

        return board
    
    def get_starting_board(self):
        return self.board
    
if __name__ == '__main__':
    print(StartingBoard().get_starting_board())