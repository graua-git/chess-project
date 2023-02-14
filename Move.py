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
        self.board_state = board
        
        self.piece = None
        self.from_coord = None
        self.to_coord = None

        # Set of true/false statements for specific move types
        self.properties = {
            'castle': self.notation[0] == 'O',
            'check': '+' in self.notation or '#' in self.notation,
            'takes': 'x' in self.notation,
            'promotion': '=' in self.notation
        }
        self.required_x = None
        self.required_y = None
        
        self._process_notation()

    def __repr__(self):
        return self.notation
    
    def get_castle_side(self):
        return self.castle_side
    
    def set_properties(self, **kwargs):
        """
        Takes the following key/value pairs to adjust properties
        castle: if the king castled on either side
        check: if the opponent is now in check
        takes: if the opponents piece was taken
        promotion: if the pawn has just promoted
        """
        for key, value in kwargs.items():
            self.properties[key] = value

    def _process_notation(self) -> None:
        """
        Fills in the missing values for Move, based on self.notation
        """
        temp_notation = self.notation

        # Castle
        if self.properties['castle']:
            self.castle_side = 'short' if self.notation == 'O-O' else 'long'
            symbol = 'K'
            return
        # Pawn move
        if not temp_notation[0].isupper():
            symbol = 'P'
        # Other piece move
        else:
            symbol = temp_notation[0]
            temp_notation = temp_notation[1:]

        # Remove + or # from notation
        if self.properties['check']:
            temp_notation = temp_notation[:-1]
        
        # Store promotion piece and remove given notation
        if self.properties['promotion']:
            self.promotion_piece = temp_notation[-1]
            temp_notation = temp_notation[:-2]

        # Get to coord
        square = temp_notation[-2:]
        self.to_coord = self._convert_chess_notation(square)
        temp_notation = temp_notation[:-2]

        # Find required x or y coordinate
        if temp_notation:
            val = temp_notation[0]
            letters = 'abcdefgh'
            nums = '12345678'
            if val in letters:
                self.required_x = letters.index(val)
            elif val in nums:
                self.required_y = int(val) - 1
        
        # Find piece
        self._find_piece(symbol)

    def _find_piece(self, symbol: str):
        for row in self.board_state:
            for piece in row:
                if self._correct_piece(piece, symbol):
                    if self.to_coord in piece.get_sees():
                        self.piece = piece
                        self.from_coord = piece.get_position()
                        return
        raise InvalidMoveError

    def _correct_piece(self, piece: Piece, symbol: str) -> bool:
        """
        Returns true if piece matches piece to move 
        """
        if piece is None:
            return False
        if self.required_x or self.required_y:
            if self.required_x == piece.get_position().x:
                return piece.get_symbol() == symbol and piece.get_team() == self.team
            if self.required_y == piece.get_position().y:
                return piece.get_symbol() == symbol and piece.get_team() == self.team
            return False
        return piece.get_symbol() == symbol and piece.get_team() == self.team

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