

class InvalidCoordError(Exception):
    pass

class Coord:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y
        self._notation = self._set_notation()

    def __repr__(self):
        return self._notation
    
    def __eq__(self, other):
        if isinstance(other, Coord):
            return self._notation == other._notation
        elif isinstance(other, str):
            return self._notation == other
        return False
    
    def x(self) -> int:
        return self._x
    
    def y(self) -> int:
        return self._y
    
    def notation(self) -> str:
        return self._notation
    
    def _set_notation(self) -> str:
        letters = 'abcdefgh'
        if self._x > 7 or self._x < 0 or self._y > 7 or self._y < 0:
            raise InvalidCoordError
        return letters[self._x] + str(self._y + 1)
