# Definition for a Chess Game class

from Piece import Piece
from Coord import Coord

#from Functions import *

class InvalidMoveError(Exception):
    pass

class ChessGame():
    def __init__(self, moves: str = None):
        self.board = self.init_new_board()
        self.turn = 'White'
        self.winner = None
    
    def init_new_board(self):
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
    
    def get_material_difference(self):
        """
        Returns the difference in material value between Black and White
        Positive for White, negative for Black
        """
        result = 0
        for row in self.board:
            for square in row:
                if square is not None:
                    val = square.get_value()
                    if square.get_team() == 'Black':
                        val = -val
                else:
                    val = 0
                result += val
        return result
    
    def make_move(self, from_coord: Coord, to_coord: Coord):
        """
        Moves one piece from one square to another, if the move is legal
        from_coord: Tuple coordinates
        to_coord: Tuple coordinates
        return: None, alters chess board if move is legal, raises error otherwise
        """
    
        piece = self.board[from_coord.x][from_coord.y]

        # Check if piece on from_coord
        try:
            if piece == None:
                raise InvalidMoveError
        except InvalidMoveError:
            print("Exception occured: No Piece on {}".format(from_coord))
            return

        # Check if piece belongs to player whose turn it is
        try:
            if piece.get_team() != self.turn:
                raise InvalidMoveError
        except InvalidMoveError:
            print("Exception occured: Not the current player's turn")
            return
        
        # Check if it is a legal move
        legal_moves = self.get_legal_moves(piece)
        cont = False
        try:
            if to_coord not in legal_moves:
                raise InvalidMoveError
        except InvalidMoveError:
            print("Exception occured: Illegal move from {} to {}".format(piece, to_coord))
            return

        # Move piece
        piece.set_position(to_coord)
        self.board[from_coord.x][from_coord.y] = None
        self.board[to_coord.x][to_coord.y] = piece

        # Switch turns
        if self.turn == 'White':
            self.turn = 'Black'
        else:
            self.turn = 'White'

    def get_legal_moves(self, piece: Piece):
        """
        Returns list of coordinates to represent legal squares piece can move to
        piece: Piece to move
        """
        primary_legal_moves = piece.legal_moves()
        return primary_legal_moves

    def __repr__(self):
        """
        Converts ChessGame into readable string
        """
        result = ''
        for y in reversed(range(8)):
            for x in range(8):
                result += str(self.board[x][y])
                if self.board[x][y] == None:
                    result += '  '
                result += ', '
            result += (' \n \n')
        return result


if __name__ == '__main__':
    game = ChessGame()
    print(game)
    print(game.get_material_difference())
    game.make_move(Coord(4, 1), Coord(4, 3))
    game.make_move(Coord(3, 6), Coord(3, 4))
    print(game)
    game.make_move(Coord(4, 3), Coord(3, 4))
    print(game)
