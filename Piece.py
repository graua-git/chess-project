# Definition for Piece class

from Coord import Coord
from Functions import *

class Piece:
    def __init__(self, name: str, team: str, value: int, position: Coord):
        self.name = name
        self.team = team
        self.value = value
        self.position = position

    def __repr__(self):
        return self.team[0] + ' ' + self.name[0:2] + self.position.chess
    
    def get_team(self):
        return self.team

    def get_value(self):
        return self.value
    
    def get_position(self):
        return self.position
    
    def set_position(self, position):
        """
        Sets new position for piece
        position: Tuple representing list coordinates
        """
        self.position = position

    def legal_moves(self) -> list:
        """
        Gets first set of legal moves based on piece's movement
        """
        return eval('self._' + self.name.lower() + '_moves()')
    
    def _pawn_moves(self) -> list:
        """
        Gets first set of legal pawn moves based on piece's movement
        """
        result = []
        # If white
        if self.team == 'White':
            direction = 1  # Direction pawn is moving
        else:
            direction = -1
        # If pawn hasn't moved
        if (self.position.y == 1 and direction == 1) or (self.position.y == 6 and direction == -1):
            result.append(Coord(self.position.x, self.position.y + 2 * direction))
        for i in range(-1, 2):
            # Don't add if pawn would go out of bounds
            if self.position.x + i >= 0 and self.position.x + i <= 7:
                result.append(Coord(self.position.x + i, self.position.y + direction))
        return result
    
    def _knight_moves(self) -> list:
        """
        Gets first set of legal knight moves based on piece's movement
        """


if __name__ == '__main__':
    game = Piece('Bishop', 'Black', (0, 2))
    print(game)