from Piece import Piece
from Coord import Coord

class InvalidMoveError(Exception):
    pass

class InvalidNotationError(Exception):
    pass

class Move:
    def __init__(self, notation: str, team: str, board: list):
        self.notation = notation
        self.team = team
        self.piece = None
        self.from_coord = None
        self.to_coord = None
        self.castle = None
        self._process_notation(self.notation, board)

    def _process_notation(self, move: str, board: list) -> None:
        # Pawn move
        if len(move) == 2 or not move[0].isupper():
            symbol = 'P'
        # Castles
        elif move[0] == 'O':
            if len(move) == 3:
                self.castle = 'short'
            else:
                self.castle = 'long'
            return
        # Standard piece move
        else:
            symbol = move[0]
        self.to_coord = self._convert_chess_notation(move[-2:])
        # Find piece
        for row in board:
            for piece in row:
                if piece is not None:
                    if piece.get_symbol() == symbol and piece.get_team() == self.team:
                        if self.to_coord in piece.get_sees():
                            self.piece = piece
                            self.from_coord = piece.get_position()
                            return
        raise InvalidMoveError
    
    def _convert_chess_notation(self, square: str) -> Coord:
        """
        square: string representing chess notation
        returns: Coord representing location on board
        """
        letters = 'abcdefgh'
        x, y = square[0], int(square[1]) - 1
        if len(square) != 2 or x not in letters or y < 0 or y > 7:
            raise InvalidNotationError
        return Coord(letters.index(x), y)