from Coord import *
from Piece import *
from Board import *

class InvalidMoveError(Exception):
    pass

class InvalidNotationError(Exception):
    pass

class Move:
    def __init__(self, board_state: Board, turn: str, move):
        """
        board_state: Board in its current state
        move EITHER str, chess move notation || OR tuple, (from_coord: Coord, to_coord: Coord)
        """
        self._board_state = board_state
        self._piece = None
        self._turn = turn
        self._notation = None
        self._from_coord = None
        self._to_coord = None

        self.required_x = None
        self.required_y = None
        
        if isinstance(move, str):
            self._notation = move
            self._properties = {
                'castle': self._notation[0] == 'O',
                'check': '+' in self._notation or '#' in self._notation,
                'takes': 'x' in self._notation,
                'promotion': '=' in self._notation
            }
            self._process_notation()

        elif isinstance(move, tuple):
            self._from_coord, self._to_coord = move
            self._notation = self._create_notation(self._to_coord, self._from_coord)
            self._properties = {
                'castle': self._notation[0] == 'O',
                'check': '+' in self._notation or '#' in self._notation,
                'takes': 'x' in self._notation,
                'promotion': '=' in self._notation
            }
        else:
            raise InvalidMoveError
        
        self._board_state.move_piece(self._from_coord, self._to_coord)
        
    def __repr__(self):
        if self._notation:
            return self._notation
        else:
            return self._from_coord, self._to_coord
    
    def board_state(self):
        """
        returns board in its current state
        """
        return self._board_state
    
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
        temp_notation = self._notation

        # Castle
        if self._properties['castle']:
            self._castle_side = 'short' if temp_notation == 'O-O' else 'long'
            symbol = 'K'
            self._castle(self.castle_side)
        # Pawn move
        if not temp_notation[0].isupper():
            symbol = 'P'
        # Other piece move
        else:
            symbol = temp_notation[0]
            temp_notation = temp_notation[1:]

        # Remove + or # from notation
        if self._properties['check']:
            temp_notation = temp_notation[:-1]
        
        # Store promotion piece and remove given notation
        if self._properties['promotion']:
            self.promotion_piece = temp_notation[-1]
            temp_notation = temp_notation[:-2]

        # Get to coord
        square = temp_notation[-2:]
        self._to_coord = self._convert_chess_notation(square)
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
        self._from_coord = self._find_piece(symbol, self._turn)

    def _find_piece(self, symbol: str, turn: str) -> Coord:
        """
        Finds piece with corresponding symbol
        symbol: symbol of piece
        turn: player whose turn it is
        return: Coord piece is coming from
        """
        for row in self._board_state:
            for piece in row:
                if self._correct_piece(piece, symbol, turn):
                    if self._to_coord in piece.sees(self._board_state.board_state()):
                        self.piece = piece
                        return piece.position()
        raise InvalidMoveError
                    
    def _correct_piece(self, piece: Piece, symbol: str, team: str) -> bool:
        """
        Returns true if piece matches piece to move 
        symbol: symbol of piece
        team: player whose turn it is
        """
        if piece is None:
            return False
        if self.required_x or self.required_y:
            if self.required_x == piece.get_position().x:
                return piece.symbol() == symbol and piece.team() == team
            if self.required_y == piece.get_position().y:
                return piece.symbol() == symbol and piece.team() == team
            return False
        return piece.symbol() == symbol and piece.team() == team
    
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

    def _castle(self):
        """
        Castle's King
        """
