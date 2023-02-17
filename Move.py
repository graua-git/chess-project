from Coord import *
from Piece import *
from Board import *

class InvalidMoveError(Exception):
    pass

class Move:
    def __init__(self, board_state: Board, move):
        """
        board_state: Board in its current state
        move EITHER str, chess move notation || OR tuple, (from_coord: Coord, to_coord: Coord)
        """
        self._board_state = board_state
        self._piece = None
        self._notation = None
        self._from_coord = None
        self._to_coord = None
        
        if isinstance(move, str):
            self._notation = move
            self._process_notation()
        elif isinstance(move, tuple):
            self._from_coord, self._to_coord = move
            self._notation = self._create_notation(self._to_coord, self._from_coord)
        else:
            raise InvalidMoveError
        
        self._properties = {
            'castle': self._notation[0] == 'O',
            'check': '+' in self._notation or '#' in self._notation,
            'takes': 'x' in self._notation,
            'promotion': '=' in self._notation
        }
        self._verify_move()
        self._make_move()
        
    def __repr__(self):
        if self._notation:
            return self._notation
        else:
            return self._from_coord, self._to_coord
    
    def board_state(self):
        """
        returns board in its current state
        """
        return self._board_state()
    
    def _create_notation(self, to_coord: Coord, from_coord: Coord) -> str:
        """
        Creates chess move notation based on the board, to_coord, and from_coord
        to_coord: Coord, coordinate piece is moving to
        from_coord: Coord piece is moving from
        return: str, chess move notation 
        """
        result = ''
        piecex, piecey = from_coord
        self._piece = self._board_state[piecex][piecey]
        if not self._piece:
            raise InvalidMoveError
        
        symbol = self._piece.symbol()
        if symbol != 'P':
            result += symbol
        result += str(to_coord)
        
        return result

    def _process_notation(self):
        """
        Gets piece, to_coord, and from_coord from chess notation and board
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
        """
        Finds piece with corresponding symbol
        symbol: symbol of piece
        """
        for row in self.board_state:
            for piece in row:
                if self._correct_piece(piece, symbol):
                    if self.to_coord in piece.get_sees():
                        self.piece = piece
                        self.from_coord = piece.get_position()
                        return
                    
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

    def _make_move(self):
        """
        Moves pieces on the board
        """
