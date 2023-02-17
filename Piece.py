from Coord import *

class Piece:
    def __init__(self, team: str, position: Coord):
        self._team = team
        self._pos = position
        self._value = 0
        self._name = self.__class__.__name__
        self._symbol = self.__class__.__name__[0]
        self._sees = []

    def __repr__(self):
        return self._team + '  ' + self._symbol
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._team == other._team
    
    def team(self) -> str:
        """
        return: str, team of the piece
        """
        return self._team

    def position(self) -> Coord:
        """
        return: Coord, position of the piece
        """
        return self._pos

    def value(self) -> int:
        """
        return: int, material value of the piece
        """
        return self._value
    
    def symbol(self) -> str:
        """
        return: str, 1 letter symbol representing piece P N B R Q or K
        """
        return self._symbol
    
    def sees(self) -> list[Coord]:
        """
        return: list of Coords piece can see based on its movement
        """
        self.update_sees()
        return self._sees
    
    def update_sees(self, board: list) -> None:
        """
        Updates what squares the piece can see
        """
        self._sees = eval(self._ + self._move_type + '_moves(self, ' + self.directions + ', board)')  
    
    def _continuous_moves(self, directions: list, board: list) -> None:
        """
        Function to get moves for bishop, rook, or queen based on which directions they can move in.
        These pieces can move continuously in their given directions
        directions: list of tuples of two ints to represent directions in which the piece can move
        board: 2D list representing current chess board
        returns: list of squares piece can see
        """
        result = []
        for direction in directions:
            curr_pos = self._pos
            # In bounds
            while True:
                next_pos = Coord(curr_pos.x + direction[0], curr_pos.y + direction[1])
                x, y = next_pos
                # Out of bounds
                if x < 0 or x > 7 or y < 0 or y > 7:
                    break
                piece = board[x][y]
                # Not occupied by piece
                if piece is None:
                    result.append(next_pos)
                    curr_pos = next_pos 
                    continue
                # Square is blocked
                if piece.team() == self._team:
                    break
                # Square can be captured
                else:
                    result.append(next_pos)
                    break
        return result

    def _single_moves(self, directions: list, board: list) -> None:
        """
        Function to get moves for knight or king based on which directions they can move in.
        These pieces can only move one square in their given direction 
        directions: list of tuples of two ints to represent directions in which the piece can move
        board: 2D list representing current chess board
        returns: list of squares piece can see
        """
        result = []
        for direction in directions:
            next_pos = Coord(self._pos.x() + direction[0], self._pos.y() + direction[1])
            x, y = next_pos
            # In bounds
            if x >= 0 and x <= 7 and y >= 0 and y <= 7:
                # Not occupied by own piece
                if board[x][y] is not None:
                    if board[x][y].team() == self._team:
                        continue
                result.append(next_pos)
        return


class Pawn(Piece):
    def __init__(self, team: str, position: Coord):
        Piece.__init__(self, team, position)
        self._value = 1
        self.en_passant = False


class Knight(Piece):
    def __init__(self, team: str, position: Coord):
        Piece.__init__(self, team, position)
        self._value = 3
        self._symbol = 'N'
        self._directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        self._move_type = 'single'


class Bishop(Piece):
    def __init__(self, team: str, position: Coord):
        Piece.__init__(self, team, position)
        self._value = 3
        self._directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        self._move_type = 'continuous'


class Rook(Piece):
    def __init__(self, team: str, position: Coord):
        Piece.__init__(self, team, position)
        self._value = 5
        self._castle = True
        self._directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        self._move_type = 'continuous'


class Queen(Piece):
    def __init__(self, team: str, position: Coord):
        Piece.__init__(self, team, position)
        self._value = 9
        self._directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self._move_type = 'continuous'


class King(Piece):
    def __init__(self, team: str, position: Coord):
        Piece.__init__(self, team, position)
        self._value = 100
        self._castle = True
        self._directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self._move_type = 'single'
