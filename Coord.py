# Definition for Coord class

class Coord():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        if x is not None and y is not None:
            letters = 'abcdefgh'
            if x < 8 and x >= 0:
                self.chess = letters[x] + str(y + 1)
            else:
                self.chess = '-' + str(y + 1)

    def __repr__(self):
        return self.chess
    
    def __eq__(self, other):
        if isinstance(other, Coord) and self.x is not None and self.y is not None:
            return self.chess == other.chess
        return False