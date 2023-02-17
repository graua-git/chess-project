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
    
    def sees(self, board: list) -> list[Coord]:
        """
        return: list of Coords piece can see based on its movement
        """
        self.update_sees(board)
        return self._sees

    def set_position(self, position: Coord) -> None:
        """
        Set's piece's position
        """
        self._pos = position
    
    def update_sees(self, board: list) -> None:
        """
        Updates what squares the piece can see
        """
        self._sees = eval('self._' + str(self._move_type) + '_moves(self._directions, board)')  
    
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
            curr_pos = self._pos
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
                if piece.team() == self._team:
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
                next_pos = Coord(self._pos.x() + direction[0], self._pos.y() + direction[1])
            except InvalidCoordError:
                continue
            x, y = next_pos
            # Not occupied by own piece
            if board[x][y] is not None:
                if board[x][y].team() == self._team:
                    continue
            result.append(next_pos)
        return result


class Pawn(Piece):
    def __init__(self, team: str, position: Coord):
        Piece.__init__(self, team, position)
        self._value = 1
        self.en_passant = False
        self._directions = []
        self._move_type = 'pawn'
    
    def _pawn_moves(self, directions: list, board: list) -> list:
        """
        Gets first set of legal pawn moves based on piece's movement
        A pawn can move forward one space (two for first move) and can only capture diagonally
        board: 2D list representing current chess board
        returns: None, updates variable self.sees
        """
        result = []
        # Set direction pawn is moving
        if self._team == 'W':
            direction = 1  # Direction pawn is moving
        else:
            direction = -1

        # If pawn hasn't moved
        
        for i in range(-1, 2):
            try:
                next_pos = Coord(self._pos.x() + i, self._pos.y() + direction)
            except InvalidCoordError:
                continue
            x, y = next_pos
            # If diagonal, don't add unless there is an oposing piece
            if i != 0:
                if board[x][y] is None:
                    continue
                elif board[x][y].team() == self.team:
                    continue
            # If straight, don't add unless space is empty
            else:
                if board[x][y]:
                    continue
                # If next square is empty, add move 2 forward if piece hasn't move yet
                if y < 7:
                    if board[x][y + direction] is None:
                        if (self._pos.y() == 1 and direction == 1) or (self._pos.y() == 6 and direction == -1):
                            result.append(Coord(self._pos.x(), self._pos.y() + 2 * direction))
            result.append(next_pos)
        return result


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
