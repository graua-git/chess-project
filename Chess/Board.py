from Chess.Coord import Coord
from Chess.Piece import *
import json


class Board:
    def __init__(self, board_state: list = None, turn: str = 'W'):
        """
        board_state: 2D list of Pieces representing chess board, optional
        turn: str, 'W' or 'B' for whoevers turn it is, 'W' by default
        """
        self.board_state = board_state
        if not self.board_state:
            self.board_state = self.starting_board()
        self.turn = turn
        self.w_piece_ref = []
        self.b_piece_ref = []
        self.set_piece_ref()
    
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

    def toJSON(self):
        result = []
        for y in reversed(range(8)):
            new_row = []
            for x in range(8):
                piece = self.board_state[x][y]
                if not piece:
                    new_row.append(json.dumps({"name": "None", "team": "None"}))
                else:
                    new_row.append(piece.toJSON())
            result.append(new_row)
        return json.dumps(result, indent=4)
    
    # ------------------------------------------- Getters -------------------------------------------
    def get_board_state(self):
        """
        Returns 2D list representing the board
        """
        return self.board_state

    def get_turn(self):
        """
        Returns current player's turn
        """
        return self.turn
    
    def get_white_pieces(self):
        """
        Returns list of all white pieces still on the board
        """
        return self.w_piece_ref
    
    def get_black_pieces(self):
        """
        Returns list of all black pieces still on the board
        """
        return self.b_piece_ref

    def switch_turns(self):
        """
        Switches player's turn
        """
        self.turn = 'W' if self.turn == 'B' else 'B'
        return
    
    def add_piece(self, piece: Piece, team: str, coord: Coord):
        """
        Adds a piece to the board
        piece: Piece, piece to add
        team: str, 'W' or 'B' representing team
        coord, Coord, where to put the piece
        """
        if team == 'W':
            self.w_piece_ref.append(piece)
        else:
            self.b_piece_ref.append(piece)
        self.board_state[coord.x()][coord.y()] = piece
        return

    def set_piece_ref(self) -> None:
        """
        Sets list of pieces to be used a reference for both black and white
        """
        for row in self.board_state:
            for piece in row:
                if not piece:
                    continue
                if piece.get_team() == 'W':
                    self.w_piece_ref.append(piece)
                else:
                    self.b_piece_ref.append(piece)

    def move_piece(self, from_coord: Coord, to_coord: Coord, turn_number: int) -> None:
        """
        Moves piece from from_coord to to_coord
        from_coord: Coordinate on chess board to represent starting position
        to_coord: Coordinate on chess board to represent ending position
        """
        if 'O-O' in to_coord:
            return
        piece_to_remove = self.board_state[to_coord.x()][to_coord.y()]
        if piece_to_remove:
            self.remove_piece(piece_to_remove)

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

    def remove_piece(self, piece: Piece) -> None:
        """
        Removes a piece from the board and from the reference list
        piece, Piece, piece to remove
        """
        team = piece.get_team()
        x, y = piece.get_position()
        self.board_state[x][y] = None
        if team == 'W':
            self.w_piece_ref.remove(piece)
        else:
            self.b_piece_ref.remove(piece)
                    
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
        turn_number: int, current turn number
        team: str, team whose king we are checking if is in check
        """
        # Find King
        piece_list = self.w_piece_ref if team == 'W' else self.b_piece_ref
        enemy_piece_list = self.b_piece_ref if team == 'W' else self.w_piece_ref

        for piece in piece_list:
            if isinstance(piece, King) and piece.get_team() == team:
                king_location = piece.get_position()
                break
        
        for piece in enemy_piece_list:
            piece.update_sees(self.board_state, turn_number, piece_list)
            if king_location in piece.get_sees(self.board_state, turn_number):
                return True
    
    def update_all_sees(self, turn_number: int) -> None:
        """
        Updates all pieces sees list
        turn_number: int, current turn number
        """
        for piece in self.w_piece_ref:
            if isinstance(piece, King):
                w_king_ref = self.w_piece_ref.index(piece)
                continue
            piece.update_sees(self.board_state, turn_number, self.b_piece_ref)
        for piece in self.b_piece_ref:
            if isinstance(piece, King):
                b_king_ref = self.b_piece_ref.index(piece)
                continue
            piece.update_sees(self.board_state, turn_number, self.w_piece_ref)

        self.w_piece_ref[w_king_ref].update_sees(self.board_state, turn_number, self.b_piece_ref)
        self.b_piece_ref[b_king_ref].update_sees(self.board_state, turn_number, self.w_piece_ref)
