from Chess.Coord import *
import json

class Piece:
    def __init__(self, team: str, position: Coord):
        self.name = self.__class__.__name__
        self.team = team
        self.pos = position
        self.value = 0
        self.symbol = self.__class__.__name__[0]
        self.sees = []
        self.turn_number_ref = 0

    def __repr__(self):
        return self.team + '  ' + self.symbol
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.team == other.team and self.pos == other.pos
    
    # ------------------------------------------- Getters -------------------------------------------
    def get_team(self) -> str:
        """
        Returns team of the piece
        """
        return self.team

    def get_position(self) -> Coord:
        """
        Returns position of the piece
        """
        return self.pos

    def get_value(self) -> int:
        """
        Returns material value of the piece
        """
        return self.value
    
    def get_name(self) -> str:
        """
        Returns str, name of piece
        """
        return self.name

    def get_symbol(self) -> str:
        """
        Returns str, 1 letter symbol representing piece P N B R Q or K
        """
        return self.symbol
    
    def get_sees(self, board: list, turn_number: int) -> list[Coord]:
        """
        Returns list of Coords piece can see based on its movement
        """
        return self.sees

    # ------------------------------------------- Setters -------------------------------------------
    def set_position(self, position: Coord) -> None:
        """
        Set's piece's position
        position: Coord, new position of piece
        """
        self.pos = position
    
    def update_sees(self, board: list, turn_number: int, enemy_piece_list: list) -> None:
        """
        Updates what squares the piece can see
        board: list, 2D array representing where pieces are
        turn_number: int, current turn number
        enemypiece_list: list, list referencing enemy pieces (for king moves)
        """
        self.turn_number_ref = turn_number
        parameters = '_moves(self.directions, board)'
        if self.move_type == 'king':
            parameters = '_moves(self.directions, enemy_piece_list, board)'
        self.sees = eval('self._' + str(self.move_type) + parameters)  
    
    def _continuous_moves(self, directions: list, board: list) -> list:
        """
        Function to get moves for bishop, rook, or queen based on which directions they can move in.
        These pieces can move continuously in their given directions
        directions: list of tuples of two ints to represent directions in which the piece can move
        board: 2D list representing current chess board
        returns: list of squares piece can see
        """
        result = []
        for direction in directions:
            curr_pos = self.pos
            # In bounds
            while True:
                try:
                    next_pos = Coord(curr_pos.x() + direction[0], curr_pos.y() + direction[1])
                except InvalidCoordError:
                    break
                x, y = next_pos
                piece = board[x][y]
                # Not occupied by piece
                if piece is None:
                    result.append(next_pos)
                    curr_pos = next_pos 
                    continue
                # Square is blocked
                if piece.get_team() == self.team:
                    break
                # Square can be captured
                else:
                    result.append(next_pos)
                    break
        return result

    def _single_moves(self, directions: list, board: list) -> list:
        """
        Function to get moves for knight or king based on which directions they can move in.
        These pieces can only move one square in their given direction 
        directions: list of tuples of two ints to represent directions in which the piece can move
        board: 2D list representing current chess board
        returns: list of squares piece can see
        """
        result = []
        for direction in directions:
            try:
                next_pos = Coord(self.pos.x() + direction[0], self.pos.y() + direction[1])
            except InvalidCoordError:
                continue
            x, y = next_pos
            # Not occupied by own piece
            if board[x][y] is not None:
                if board[x][y].get_team() == self.team:
                    continue
            result.append(next_pos)
        return result


class Pawn(Piece):
    def __init__(self, team: str, position: Coord):
        Piece.__init__(self, team, position)
        self.value = 1
        self.en_passant_turn = 0
        self.directions = [-1, 0, 1]
        self.move_type = 'pawn'
    
    def get_en_passant(self) -> int:
        """
        Returns turn number that the pawn moved two squares for en passant
        """
        return self.en_passant_turn
    
    def set_en_passant(self, turn_number: int) -> None:
        """
        Set's turn that pawn can be taken by en passant
        """
        self.en_passant_turn = turn_number
        if self.team == 'B':
            self.en_passant_turn += 1

    def check_en_passant(self, board: list, next_pos: Coord, direction: int) -> bool:
        """
        Returns True if pawn can be en passant, False otherwise
        board: 2D list representing current chess board
        next_pos: coordinate pawn would land on if takes
        direction: direction pawn is moving
        """
        x, y = next_pos
        y -= direction
        pawn = board[x][y]
        if not pawn:
            return False
        if self.team == pawn.get_team():
            return False
        if not isinstance(pawn, Pawn):
            return False
        
        return self.turn_number_ref == pawn.get_en_passant()

    def _pawn_moves(self, directions: list, board: list) -> list:
        """
        Function to get moves for a pawn based on which directions they can move in.
        A pawn can move forward one space (two for first move) and can only capture diagonally
        directions: list of ints to represent directions in which the piece can move horizontally
        board: 2D list representing current chess board
        """
        result = []
        # Set direction pawn is moving
        if self.team == 'W':
            forward = 1  # Direction pawn is moving
        else:
            forward = -1
        
        for direction in directions:
            try:
                next_pos = Coord(self.pos.x() + direction, self.pos.y() + forward)
            except InvalidCoordError:
                continue
            x, y = next_pos
            # If diagonal, don't add unless there is an oposing piece
            if direction != 0:
                if board[x][y] is None:
                    if not self.check_en_passant(board, next_pos, forward):
                        continue
                elif board[x][y].get_team() == self.team:
                    continue
            # If straight, don't add unless space is empty
            else:
                if board[x][y]:
                    continue
                # If next square is empty, add move 2 forward if piece hasn't move yet
                if y < 7:
                    if board[x][y + forward] is None:
                        if (self.pos.y() == 1 and forward == 1) or (self.pos.y() == 6 and forward == -1):
                            result.append(Coord(self.pos.x(), self.pos.y() + 2 * forward))
            result.append(next_pos)
        return result


class Knight(Piece):
    def __init__(self, team: str, position: Coord):
        Piece.__init__(self, team, position)
        self.value = 3
        self.symbol = 'N'
        self.directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        self.move_type = 'single'


class Bishop(Piece):
    def __init__(self, team: str, position: Coord):
        Piece.__init__(self, team, position)
        self.value = 3
        self.directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        self.move_type = 'continuous'


class Rook(Piece):
    def __init__(self, team: str, position: Coord):
        Piece.__init__(self, team, position)
        self.value = 5
        self.castle = True
        self.directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        self.move_type = 'continuous'
    
    def set_castle(self, val: bool) -> None:
        self.castle = val

    def get_castle(self):
        return self.castle


class Queen(Piece):
    def __init__(self, team: str, position: Coord):
        Piece.__init__(self, team, position)
        self.value = 9
        self.directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.move_type = 'continuous'


class King(Piece):
    def __init__(self, team: str, position: Coord):
        Piece.__init__(self, team, position)
        self.value = 100
        self.castle = True
        self.directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.move_type = 'king'

    def set_castle(self, val: bool) -> None:
        self.castle = val

    def get_castle(self):
        return self.castle

    def _king_moves(self, directions: list, piece_list: list, board: list) -> list:
        """
        Returns first set of legal King moves based on piece's movement
        A king can move a single space in any direction
        A king can also castle, moving 2 spaces towards a rook, having the rook come over it
        directions: list of tuples of two ints to represent directions in which the piece can move
        piece_list: list of enemy pieces
        board: 2D list representing current chess board
        """
        result = self._single_moves(directions, board)
        y = 0 if self.team == 'W' else 7
        # Add castle possibility
        if self.castle:
            if self.can_castle('short', piece_list, board, y):
                result.append('O-O')
            if self.can_castle('long', piece_list, board, y):
                result.append('O-O-O')

        return result
    
    def can_castle(self, side: str, piece_list: list, board, y: int) -> bool:
        """
        Returns True if king can castle to side, False otherwise
        side: 'short' or 'long' for which side to castle
        board: 2D list representing current chess board
        y: y-coord of the king
        """
        if side == 'short':
            x_vals = [5, 6]
            check_x_vals = [4, 5, 6]
            rook: Rook = board[7][y]
        if side == 'long':
            x_vals = [3, 2, 1]
            check_x_vals = [4, 3, 2]
            rook: Rook = board[0][y]
        
        # Check rook
        if not isinstance(rook, Rook):
            return False
        if not rook.castle:
            return False
        
        # Check squares for empty and vision
        for x in x_vals:
            if board[x][y]:
                return False
            
        # Check to see if King castles out of, into, or through check
        for x in check_x_vals:
            square = Coord(x, y)
            opposing_team = 'W' if self.team == 'B' else 'B'
            if self.check_visibility(opposing_team, piece_list, board, square):
                return False

        return True
    
    def check_visibility(self, opposing_team: str, piece_list: list, board: list, square: Coord) -> bool:
        """
        Returns True if opposing_team has a piece that can see square, False otherwise
        opposing_team: str, team who were checking
        board: 2D list representing chess board
        square: Coord, square we're checking to see if opposing team can see
        """
        for piece in piece_list:
            if isinstance(piece, King):
                pos = piece.get_position()
                if opposing_team == 'W':
                    return pos == 'g7' or pos == 'b7'
                else:
                    return pos == 'g2' or pos == 'b2'
            if square in piece.get_sees(board, self.turn_number_ref):
                return True
        return False
