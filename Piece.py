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
        return self._team

    def position(self) -> Coord:
        return self._pos

    def value(self) -> int:
        return self._value
    
    def sees(self) -> list:
        return self._sees


class Pawn(Piece):
    def __init__(self, team: str, position: str):
        Piece.__init__(self, team, position)
        self._value = 1
        self.en_passant = False


class Knight(Piece):
    def __init__(self, team: str, position: str):
        Piece.__init__(self, team, position)
        self._value = 3
        self._symbol = 'N'


class Bishop(Piece):
    def __init__(self, team: str, position: str):
        Piece.__init__(self, team, position)
        self._value = 3


class Rook(Piece):
    def __init__(self, team: str, position: str):
        Piece.__init__(self, team, position)
        self._value = 5
        self.castle = True


class Queen(Piece):
    def __init__(self, team: str, position: str):
        Piece.__init__(self, team, position)
        self._value = 9


class King(Piece):
    def __init__(self, team: str, position: str):
        Piece.__init__(self, team, position)
        self._value = 100
        self.castle = True
