LETTERS = 'abcdefgh'

class InvalidCoordError(Exception):
    pass

class Coord:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y
        self._notation = self._set_notation()

    def __repr__(self):
        return self._notation
    
    def __iter__(self):
        return iter((self._x, self._y))
    
    def __eq__(self, other):
        if isinstance(other, Coord):
            return self._notation == other._notation
        elif isinstance(other, str):
            return self._notation == other
        return False

    def x(self) -> int:
        """
        Returns x coord
        """
        return self._x
    
    def y(self) -> int:
        """
        Returns y coord
        """
        return self._y
    
    def notation(self) -> str:
        """
        Returns chess coordinate notation
        """
        return self._notation
    
    def _set_notation(self) -> str:
        """
        Creates chess square notation based on x, y coordinates 
        return: str, notation
        """
        if self._x > 7 or self._x < 0 or self._y > 7 or self._y < 0:
            raise InvalidCoordError
        return LETTERS[self._x] + str(self._y + 1)
