from Coord import Coord
from Piece import *


class Board:
    def __init__(self, board_state: list = None, turn: str = 'W'):
        """
        board_state: 2D list of Pieces representing chess board, optional
        turn: str, 'W' or 'B' for whoevers turn it is, 'W' by default
        """
        self._board_state = board_state
        if not self._board_state:
            self._board_state = self._starting_board()
        self._turn = 'W'
    
    def __repr__(self):
        result = '------------------------------------------------ \n'
        for y in reversed(range(8)):
            for x in range(8):
                result += str(self._board_state[x][y])
                result += ', '
            result += (' \n \n')
        return result + '------------------------------------------------'

    def __iter__(self):
        return iter(self._board_state)
    
    def __getitem__(self, index):
         return self._board_state[index]
    
    def __setitem__(self, index, item):
        self._board_state[index] = item
    
    def board_state(self):
        return self._board_state

    def turn(self):
        return self._turn
    
    def switch_turns(self):
        """
        Switches player's turn
        """
        if self._turn == 'W':
            self._turn = 'B'
        else:
            self._turn = 'W'

    def move_piece(self, from_coord: Coord, to_coord: Coord):
        """
        moves piece from from_coord to to_coord
        from_coord: Coordinate on chess board to represent starting position
        to_coord: Coordinate on chess board to represent ending position
        """
        piece = self._board_state[from_coord.x()][from_coord.y()]
        piece.set_position(to_coord)
        self._board_state[from_coord.x()][from_coord.y()] = None
        self._board_state[to_coord.x()][to_coord.y()] = piece
        return

    def _starting_board(self) -> list:
        """
        Creates a starting chess board
        returns: 2D List of pieces
        """
        board = [[None for x in range(8)] for y in range(8)]

        # Pawns
        for square in range(8):
            board[square][1] = Pawn('W', Coord(square, 1))
            board[square][6] = Pawn('B', Coord(square, 6))
        
        # Other pieces
        teams = [('W', 0), ('B', 7)]
        for team, y in teams:
            board[0][y] = Rook(team, Coord(0, y))
            board[1][y] = Knight(team, Coord(1, y))
            board[2][y] = Bishop(team, Coord(2, y))
            board[3][y] = Queen(team, Coord(3, y))
            board[4][y] = King(team, Coord(4, y))
            board[5][y] = Bishop(team, Coord(5, y))
            board[6][y] = Knight(team, Coord(6, y))
            board[7][y] = Rook(team, Coord(7, y))

        return board