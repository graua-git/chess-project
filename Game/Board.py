from Coord import Coord
from Piece import *


class Board:
    def __init__(self, board_state: list = None, turn: str = 'W'):
        """
        board_state: 2D list of Pieces representing chess board, optional
        turn: str, 'W' or 'B' for whoevers turn it is, 'W' by default
        """
        self.board_state = board_state
        if not self.board_state:
            self.board_state = self.starting_board()
        self.turn = 'W'
    
    def __repr__(self):
        result = '------------------------------------------------ \n'
        for y in reversed(range(8)):
            for x in range(8):
                result += str(self.board_state[x][y])
                result += ', '
            result += (' \n \n')
        return result + '------------------------------------------------'

    def __iter__(self):
        return iter(self.board_state)
    
    def __getitem__(self, index):
         return self.board_state[index]
    
    def __setitem__(self, index, item):
        self.board_state[index] = item
    
    def get_board_state(self):
        return self.board_state

    def get_turn(self):
        return self.turn
    
    def switch_turns(self):
        """
        Switches player's turn
        """
        self.turn = 'W' if self.turn == 'B' else 'B'

    def move_piece(self, from_coord: Coord, to_coord: Coord, turn_number: int) -> None:
        """
        moves piece from from_coord to to_coord
        from_coord: Coordinate on chess board to represent starting position
        to_coord: Coordinate on chess board to represent ending position
        """
        if 'O-O' in to_coord:
            return
        piece = self.board_state[from_coord.x()][from_coord.y()]
        piece.set_position(to_coord)
        self.board_state[from_coord.x()][from_coord.y()] = None
        self.board_state[to_coord.x()][to_coord.y()] = piece
        self.switch_turns()

        if isinstance(piece, Rook) or isinstance(piece, King):
            piece._castle = False
        
        if isinstance(piece, Pawn):
            if abs(from_coord.y() - to_coord.y()) == 2:
                piece.set_en_passant(turn_number)
        return

    def starting_board(self) -> list:
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
    
    def in_check(self, turn_number: int, team: str) -> True:
        """
        Returns True if the player whose turn it is is in check, False otherwise
        """
        # Find King
        for row in self.board_state:
            for piece in row:
                if piece:
                    if isinstance(piece, King) and piece.get_team() == team:
                        king_location = piece.get_position()
                        break
        
        for row in self.board_state:
            for piece in row:
                if piece:
                    if piece.get_team() != team:
                        if king_location in piece.get_sees(self.board_state, turn_number):
                            return True

    def update_all_sees(self, turn_number: int) -> None:
        for row in self.board_state:
            for piece in row:
                if piece:
                    piece.update_sees(self.board_state, turn_number)