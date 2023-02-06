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
    
    # ----------------------------------- Getters and Setters -----------------------------------
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

    # ------------------------------------- Get Legal Moves -------------------------------------
    def legal_moves(self, board: list) -> list:
        """
        Gets first set of legal moves based on piece's movement
        """
        return eval('self._' + self.name.lower() + '_moves(board)')
    
    # -------------------------------------- Pawn --------------------------------------
    def _pawn_moves(self, board) -> list:
        """
        Gets first set of legal pawn moves based on piece's movement
        A pawn can move forward one space (two for first move) and can only capture diagonally
        """
        result = []
        # Set direction pawn is moving
        if self.team == 'White':
            direction = 1  # Direction pawn is moving
        else:
            direction = -1

        # If pawn hasn't moved
        
        for i in range(-1, 2):
            next_pos = Coord(self.position.x + i, self.position.y + direction)
            # Don't add if pawn would go out of bounds
            if next_pos.x < 0 and next_pos.x > 7:
                continue
            # If diagonal, don't add unless there is an oposing piece
            if i != 0:
                if board[next_pos.x][next_pos.y] is None:
                    continue
                elif board[next_pos.x][next_pos.y].get_team() == self.team:
                    continue
            # If straight, don't add unless space is empty
            else:
                if board[next_pos.x][next_pos.y] is not None:
                    continue
                # If next square is empty, add move 2 forward if piece hasn't move yet
                elif board[next_pos.x][next_pos.y + direction] is None:
                    if (self.position.y == 1 and direction == 1) or (self.position.y == 6 and direction == -1):
                        result.append(Coord(self.position.x, self.position.y + 2 * direction))
            result.append(next_pos)

        return result
    
    # -------------------------------------- Pawn --------------------------------------
    def _knight_moves(self, board: list) -> list:
        """
        Gets first set of legal knight moves based on piece's movement
        A knight can move 2 in a direction, 1 in another, in any direction, and can jump over other pieces
        """
        result = []
        # Get all 8 permutations of directions
        directions = [2, -2, 1, -1]
        permutations = []

        for i in range(len(directions)):
            for j in range(len(directions)):
                if abs(directions[i]) != abs(directions[j]):
                    permutations.append((directions[i], directions[j]))
        
        for direction in permutations:
            next_pos = Coord(self.position.x + direction[0], self.position.y + direction[1])
            # In bounds
            if next_pos.x >= 0 and next_pos.x <= 7 and next_pos.y >= 0 and next_pos.y <= 7:
                # Not occupied by own piece
                if board[next_pos.x][next_pos.y] is not None:
                    if board[next_pos.x][next_pos.y].get_team() == self.team:
                        continue
                result.append(next_pos)

        return result


if __name__ == '__main__':
    game = Piece('Bishop', 'Black', Coord(0, 2))
    print(game)