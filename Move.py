from Piece import Piece
from Coord import Coord

class Move:
    def __init__(self, notation: str, team: str, board: list):
        self.notation = notation
        self.team = team
        
        if len(notation) == 0:
            return
        # Pawn move
        if len(move) == 2 or not move[0].isupper():
            symbol = 'P'
        # Castles
        elif move[0] == 'O':
            try:
                if len(move) == 3:
                    self.castle('short')
                else:
                    self.castle('long')
                return
            except InvalidMoveError:
                print('Exception made: {} cannot Castle in the current position'.format(self.turn))
        # Standard piece move
        else:
            symbol = move[0]
        to_coord = self.convert_chess_notation(move[-2:])
        # Find piece
        for row in self.board:
            for piece in row:
                if piece is not None:
                    if piece.get_symbol() == symbol and piece.get_team() == self.turn:
                        if to_coord in piece.get_sees():
                            from_coord = piece.get_position()
                            try:
                                self._move_helper(from_coord, to_coord)
                            except InvalidMoveError:
                                print('Exception made, Invalid Move: {}'.format(move))
                            return
        raise InvalidMoveError