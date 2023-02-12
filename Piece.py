# Definition for Piece class

from Coord import Coord
from Directions import Directions

from Functions import *

directions = Directions()

class Piece:
    def __init__(self, name: str, team: str, value: int, position: Coord):
        self.name = name
        self.symbol = self._create_symbol()
        self.team = team
        self.value = value
        self.position = position
        if self.symbol == 'K' or self.symbol == 'R':
            self.castle = True
        self.sees = []

    def __repr__(self):
        return self.team[0] + '  ' + self.symbol
    
    def _create_symbol(self) -> str:
        if self.name == 'Knight':
            return 'N'
        else:
            return self.name[0]

    # ----------------------------------- Getters and Setters -----------------------------------
    def get_name(self):
        return self.name
    
    def get_symbol(self):
        return self.symbol

    def get_team(self):
        return self.team

    def get_value(self):
        return self.value
    
    def get_position(self):
        return self.position
    
    def get_castle(self):
        return self.castle
    
    def get_sees(self):
        return self.sees
    
    def set_position(self, position):
        """
        Sets new position for piece
        position: Tuple representing list coordinates
        """
        self.position = position

    def set_castle(self, castle):
        self.castle = castle

    # ------------------------------------- Get Legal Moves -------------------------------------
    def legal_moves(self, board: list) -> list:
        """
        Gets first set of legal moves based on piece's movement
        board: 2D list representing current chess board
        returns: preliminary list of legal moves piece can make
        """
        self.update_sees(board)
        return self.sees
    
    def update_sees(self, board: list) -> None:
        """
        Updates self.sees with a list of legal moves based on a piece's movement
        returns: None, updates variable self.sees
        """
        eval('self._' + self.name.lower() + '_sees(board)')
    
    # -------------------------------------- Pawn --------------------------------------
    def _pawn_sees(self, board: list) -> list:
        """
        Gets first set of legal pawn moves based on piece's movement
        A pawn can move forward one space (two for first move) and can only capture diagonally
        board: 2D list representing current chess board
        returns: None, updates variable self.sees
        """
        self.sees = []
        # Set direction pawn is moving
        if self.team == 'White':
            direction = 1  # Direction pawn is moving
        else:
            direction = -1

        # If pawn hasn't moved
        
        for i in range(-1, 2):
            next_pos = Coord(self.position.x + i, self.position.y + direction)
            # Don't add if pawn would go out of bounds
            if next_pos.x < 0 or next_pos.x > 7:
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
                        self.sees.append(Coord(self.position.x, self.position.y + 2 * direction))
            self.sees.append(next_pos)

    # -------------------------------------- Knight --------------------------------------
    def _knight_sees(self, board: list) -> None:
        """
        Gets first set of legal knight moves based on piece's movement
        A knight can move 2 in a direction, 1 in another, in any direction, and can jump over other pieces
        board: 2D list representing current chess board
        returns: None, updates variable self.sees
        """
        self._single_moves(directions.knight, board)

    # -------------------------------------- Bishop --------------------------------------
    def _bishop_sees(self, board: list) -> None:
        """
        Gets first set of legal bishop moves based on piece's movement
        A bishop can move diagonally in all 4 directions
        board: 2D list representing current chess board
        returns: None, updates variable self.sees
        """
        self._continuous_moves(directions.bishop, board)

    # -------------------------------------- Rook --------------------------------------
    def _rook_sees(self, board: list) -> None:
        """
        Gets first set of legal rook moves based on piece's movement
        A rook can move horizontally or vertically in any direction
        board: 2D list representing current chess board
        returns: None, updates variable self.sees
        """
        self._continuous_moves(directions.rook, board)
    
    # -------------------------------------- Queen --------------------------------------
    def _queen_sees(self, board: list) -> None:
        """
        Gets first set of legal queen moves based on piece's movement
        A queen can move horizontally, vertically, or diagonally in any direction
        board: 2D list representing current chess board
        returns: None, updates variable self.sees
        """
        self._continuous_moves(directions.queen, board)
    
    # -------------------------------------- King --------------------------------------
    def _king_sees(self, board: list) -> None:
        """
        Gets first set of legal king moves based on piece's movement
        A king can move one square away in any direction
        board: 2D list representing current chess board
        returns: None, updates variable self.sees
        """
        self._single_moves(directions.king, board)


    def _continuous_moves(self, directions: list, board: list) -> None:
        """
        Function to get moves for bishop, rook, or queen based on which directions they can move in.
        These pieces can move continuously in their given directions
        directions: list of tuples of two ints to represent directions in which the piece can move
        board: 2D list representing current chess board
        returns: None, updates variable self.sees
        """
        self.sees = []
        for direction in directions:
            curr_pos = self.position
            # In bounds
            while True:
                next_pos = Coord(curr_pos.x + direction[0], curr_pos.y + direction[1])
                # Out of bounds
                if next_pos.x < 0 or next_pos.x > 7 or next_pos.y < 0 or next_pos.y > 7:
                    break
                piece = board[next_pos.x][next_pos.y]
                # Not occupied by piece
                if piece is None:
                    self.sees.append(next_pos)
                    curr_pos = next_pos 
                    continue
                # Square is blocked
                if piece.get_team() == self.team:
                    break
                # Square can be captured
                else:
                    self.sees.append(next_pos)
                    break

    def _single_moves(self, directions: list, board: list) -> None:
        """
        Function to get moves for knight or king based on which directions they can move in.
        These pieces can only move one square in their given direction 
        directions: list of tuples of two ints to represent directions in which the piece can move
        board: 2D list representing current chess board
        returns: None, updates variable self.sees
        """
        self.sees = []
        for direction in directions:
            next_pos = Coord(self.position.x + direction[0], self.position.y + direction[1])
            # In bounds
            if next_pos.x >= 0 and next_pos.x <= 7 and next_pos.y >= 0 and next_pos.y <= 7:
                # Not occupied by own piece
                if board[next_pos.x][next_pos.y] is not None:
                    if board[next_pos.x][next_pos.y].get_team() == self.team:
                        continue
                self.sees.append(next_pos)


if __name__ == '__main__':
    game = Piece('Bishop', 'Black', Coord(0, 2))
    print(game)