from Coord import *
from Piece import *
from Board import *
import copy

class InvalidMoveError(Exception):
    pass

class InvalidNotationError(Exception):
    pass

class Move:
    def __init__(self, board_state: Board, turn: str, turn_number: int, move):
        """
        board_state: Board in its current state
        turn: str 'W' or 'B'
        turn_number: int, turn number
        move EITHER str, chess move notation || OR tuple, (from_coord: Coord, to_coord: Coord)
        """
        self.board_state = board_state
        self.piece = None
        self.turn = turn
        self.turn_number = turn_number
        self.notation = None
        self.from_coord = None
        self.to_coord = None

        self.required_x = None
        self.required_y = None
        
        if isinstance(move, str):
            self.notation = move
            self.properties = {
                'castle': self.notation[0] == 'O',
                'check': '+' in self.notation or '#' in self.notation,
                'takes': 'x' in self.notation,
                'promotion': '=' in self.notation,
                'en passant': False
            }
            self.process_notation()

        elif isinstance(move, tuple):
            self.from_coord, self.to_coord = move
            self.notation = self.create_notation(self.from_coord, self.to_coord)
            self.properties = {
                'castle': self.notation[0] == 'O',
                'check': '+' in self.notation or '#' in self.notation,
                'takes': 'x' in self.notation,
                'promotion': '=' in self.notation,
                'en passant': False
            }
        else:
            raise InvalidMoveError
        
        if not self.properties['castle']:
            if self.left_in_check(self.board_state):
                raise InvalidMoveError
        
    def __repr__(self):
        if self.notation:
            return str(self.notation)
        else:
            return str(self.from_coord, self.to_coord)

    def get_board_state(self):
        """
        returns board in its current state
        """
        return self.board_state
    
    def create_notation(self, from_coord: Coord, to_coord: Coord) -> str:
        """
        Creates chess move notation based on the board, to_coord, and from_coord
        to_coord: Coord, coordinate piece is moving to
        from_coord: Coord piece is moving from
        return: str, chess move notation 
        """
        result = ''
        piecex, piecey = from_coord
        self.piece = self.board_state[piecex][piecey]
        if not self.piece:
            raise InvalidMoveError
        
        symbol = self.piece.get_symbol()
        if symbol != 'P':
            result += symbol
        result += str(to_coord)
        
        return result
    
    def commit_move(self) -> None:
        """
        Makes move on the board
        """
        if self.properties['castle']:
            self.castle(self.castle_side)
            self.board_state.switch_turns()

        if self.properties['takes'] and self.piece.get_symbol() == 'P':
            x, y = self.to_coord
            if not self.board_state[x][y]:
                self.properties['en passant'] = True
                self.en_passant(self.to_coord, self.turn)

        self.board_state.move_piece(self.from_coord, self.to_coord, self.turn_number)

        if self.properties['promotion']:
            self.promote(self.to_coord, self.promotion_piece)

    def process_notation(self):
        """
        Gets piece, to_coord, and from_coord from chess notation and board
        """
        temp_notation = self.notation

        # Castle
        if self.properties['castle']:
            self.castle_side = 'short' if temp_notation == 'O-O' else 'long'
            from_x = 4
            from_y = 0 if self.turn == 'W' else 7
            self.from_coord = Coord(from_x, from_y)
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
        self.to_coord = self.convert_chess_notation(square)
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
        self.from_coord = self.find_piece(symbol, self.turn)

    def find_piece(self, symbol: str, turn: str) -> Coord:
        """
        Finds piece with corresponding symbol
        symbol: symbol of piece
        turn: player whose turn it is
        return: Coord piece is coming from
        """
        for row in self.board_state:
            for piece in row:
                if self.correct_piece(piece, symbol, turn):
                    if self.to_coord in piece.get_sees(self.board_state.get_board_state(), self.turn_number):
                        self.piece = piece
                        return piece.get_position()
        raise InvalidMoveError
                    
    def correct_piece(self, piece: Piece, symbol: str, team: str) -> bool:
        """
        Returns true if piece matches piece to move 
        symbol: symbol of piece
        team: player whose turn it is
        """
        if piece is None:
            return False
        correct_symbol = piece.get_symbol()
        correct_team = piece.get_team()
        correct_pos = piece.get_position()
        if self.required_x or self.required_y:
            if self.required_x == correct_pos.x():
                return symbol == correct_symbol and team == correct_team
            if self.required_y == correct_pos.y():
                return symbol == correct_symbol and team == correct_team
            return False
        return symbol == correct_symbol and team == correct_team
    
    def convert_chess_notation(self, square: str) -> Coord:
        """
        square: string representing chess notation
        returns: Coord representing location on board
        """
        letters = 'abcdefgh'
        x, y = square[0], int(square[1]) - 1
        if len(square) != 2 or x not in letters or y < 0 or y > 7:
            raise InvalidNotationError
        return Coord(letters.index(x), y)

    def castle(self, castle_side):
        """
        Castle's King
        """
        short = castle_side == 'short'
        y = 0 if self.turn == 'W' else 7
        self.piece = self.board_state[4][y]
        self.from_coord = Coord(4, y)

        x = 6 if short else 2
        rook_from_x = 7 if short else 0
        rook_to_x = 5 if short else 3
        self.to_coord = Coord(x, y)

        # Move rook
        self.board_state.move_piece(Coord(rook_from_x, y), Coord(rook_to_x, y), self.turn_number)

    def promote(self, coord: Coord, symbol: str) -> None:
        """
        Promotes pawn at coord
        """
        team = self.turn
        if symbol == 'Q':
            piece = Queen(team, coord)
        elif symbol == 'R':
            piece = Rook(team, coord)
        elif symbol == 'B':
            piece = Bishop(team, coord)
        elif symbol == 'N':
            piece = Knight(team, coord)
        self.board_state[coord.x()][coord.y()] = piece
        return 

    def en_passant(self, to_coord: Coord, team = str) -> None:
        """
        Removes pawn captured by En passant
        """
        y_change = 1 if team == 'W' else -1
        x, y = to_coord
        self.board_state[x][y - y_change] = None
        return

    def left_in_check(self, board: Board) -> bool:
        """
        Returns True if own king was left in check, False otherwise
        """
        new_board = copy.deepcopy(board.get_board_state())
        hypothetical = Board(new_board, self.turn)
        hypothetical.move_piece(self.from_coord, self.to_coord, self.turn_number)
        return hypothetical.in_check(self.turn_number, self.piece.get_team())
