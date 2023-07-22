from Chess.Coord import *
from Chess.Piece import *
from Chess.Board import *

class InvalidMoveError(Exception):
    pass

class InvalidNotationError(Exception):
    pass

class Move:
    def __init__(self, board_state: Board, turn: str, turn_number: int, from_coord: Coord, to_coord: Coord):
        """
        board_state: Board in its current state
        turn: str 'W' or 'B'
        turn_number: int, turn number
        from_coord: Coord, coordinate piece is coming from
        to_coord: Coord, coordinate piece is going to
        """
        self.notation = None

        self.board_state = board_state
        self.piece = self.board_state[from_coord.x()][from_coord.y()]
        self.turn = turn
        self.turn_number = turn_number
        
        self.from_coord = from_coord
        self.to_coord = to_coord
        
        if 'O' not in self.to_coord:
            self.notation = self.create_notation(self.from_coord, self.to_coord)

        if self.to_coord:
            if 'O' in self.to_coord:
                self.notation = self.to_coord
                x = 6 if self.to_coord == 'O-O' else 2
                y = self.piece.get_position().y()
                self.to_coord = Coord(x, y)

        self.properties = {
            'castle': self.notation[0] == 'O',
            'takes': 'x' in self.notation,
            'promotion': '=' in self.notation,
            'en passant': False
            }
        
        if not self.properties['takes'] and 'x' not in self.notation:
            self.notation = self.update_takes(self.board_state, self.from_coord, self.to_coord)
        
        if self.properties['takes']:
            piece = board_state[to_coord.x()][to_coord.y()]
            if not piece:
                pass
            elif board_state[to_coord.x()][to_coord.y()].get_team() == self.piece.get_team():
                raise InvalidMoveError

        if not self.properties['castle']:
            if self.left_in_check(self.board_state):
                raise InvalidMoveError
        
    def __repr__(self):
        if self.notation:
            return str(self.notation)
        else:
            return str(self.from_coord) + ' to ' + str(self.to_coord)
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Move):
            return self.notation == other.notation
        elif isinstance(other, str):
            return self.notation == other
        return False
    
    def __iter__(self):
        return iter(self.notation)

    # ------------------------------------------- Getters -------------------------------------------
    def get_board_state(self):
        """
        Returns board in its current state
        """
        return self.board_state
    
    def get_piece(self):
        """
        Returns piece being moved
        """
        return self.piece

    def get_required_coord(self, from_coord: Coord, to_coord: Coord) -> str:
        """
        Returns additional characters to add to the notation from the from_coord if multiple pieces can move to the to_coord
        from_coord: Coord, coordinate piece is coming from
        to_coord: Coord, coordinate piece is going to
        """
        result = ''
        if not isinstance(self.piece, Pawn) and not isinstance(self.piece, King):
            piece_type = self.piece.__class__
            team = self.piece.get_team()
            piece_list = self.board_state.get_white_pieces() if team == 'W' else self.board_state.get_black_pieces()
            for other_piece in piece_list:
                if other_piece is self.piece:
                    continue
                if other_piece.__class__ != piece_type:
                    continue
                elif other_piece.get_team() != self.piece.get_team():
                    continue
                elif to_coord not in other_piece.get_sees(self.board_state, self.turn_number):
                    continue
                
                # Multiple pieces can see the to_coord
                if other_piece.get_position().x() == self.piece.get_position().x():
                    result += str(from_coord.y() + 1)
                else:
                    letters = 'abcdefgh'
                    result += letters[self.from_coord.x()]
        return result
    
    # ------------------------------------------- Setters -------------------------------------------
    def set_promotion_piece(self, piece: str) -> None:
        """
        Sets promotion piece to piece 'Q' 'R' 'B' or 'N', updates notation
        """
        if len(piece) != 1:
            return
        self.promotion_piece = piece
        self.notation += '=' + piece
        return
    
    def set_board(self, h_board: Board) -> None:
        """
        Sets board state to new board 
        """
        self.board_state = h_board
    
    # ------------------------------------------- Updates -------------------------------------------
    def update_takes(self, board: Board, from_coord: Coord, to_coord: Coord) -> str:
        """
        Returns new notation if piece took another one
        """
        if not from_coord or not to_coord or str(to_coord)[0] == 'O':
            return
        x, y = to_coord
        if not board[x][y]:
            return self.notation
        symbol = self.piece.get_symbol()
        if symbol == 'P':
            symbol = str(from_coord)[0]
        return symbol + 'x' + str(to_coord)
    
    def update_castles(self, notation: str):
        """
        Returns new notation if piece castled
        """
        self.properties['castle'] = 'short' if notation == 'O-O' else 'long'

    def create_notation(self, from_coord: Coord, to_coord: Coord) -> str:
        """
        Creates chess move notation based on the board, to_coord, and from_coord
        from_coord: Coord piece is moving from
        to_coord: Coord, coordinate piece is moving to
        return: str, chess move notation 
        """
        if self.piece is None:
            raise InvalidMoveError
        result = ''
        king = isinstance(self.piece, King)
        if king:
            y = 0 if self.turn == 'W' else 7
            if self.piece.get_castle():
                # Short
                if self.to_coord.x() == 6:
                    rook = self.board_state[7][y]
                    if rook:
                        if rook.get_castle():
                            return 'O-O'
                        else:
                            raise InvalidMoveError
                elif self.to_coord.x() == 2:
                    rook = self.board_state[0][y]
                    if rook:
                        if rook.get_castle():
                            return 'O-O-O'
                        else:
                            raise InvalidMoveError
        pawn = isinstance(self.piece, Pawn)
        result += self.piece.get_symbol() if not pawn else ''
        result += self.get_required_coord(from_coord, to_coord)

        if self.board_state[to_coord.x()][to_coord.y()]:
            result += str(from_coord)[0] if pawn else ''
            result += 'x'
        
        elif pawn:
            direction = 1 if self.piece.get_team() == 'W' else -1
            if self.piece.check_en_passant(self.board_state, to_coord, direction):
                result += str(from_coord)[0] + 'x'
            
        return result + str(to_coord)

    def commit_move(self) -> None:
        """
        Makes move on the board
        """
        if self.properties['castle']:
            self.castle()
            self.board_state.switch_turns()

        if self.properties['takes'] and self.piece.get_symbol() == 'P':
            x, y = self.to_coord
            if not self.board_state[x][y]:
                self.properties['en passant'] = True
                self.en_passant(self.to_coord, self.turn)

        self.board_state.move_piece(self.from_coord, self.to_coord, self.turn_number)

        if isinstance(self.piece, King) or isinstance(self.piece, Rook):
            self.piece.set_castle(False)

        if self.properties['promotion']:
            self.promote(self.to_coord, self.promotion_piece)
                    
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
        Returns Coord representing location on board
        square: string representing chess notation
        """
        letters = 'abcdefgh'
        x, y = square[0], int(square[1]) - 1
        if len(square) != 2 or x not in letters or y < 0 or y > 7:
            raise InvalidNotationError
        return Coord(letters.index(x), y)

    # ---------------------------------------- Special Moves ----------------------------------------
    def castle(self):
        """
        Castles King
        """
        short = self.to_coord.x() == 6
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
        self.board_state.remove_piece(Pawn(team, coord))
        if symbol == 'Q':
            piece = Queen(team, coord)
        elif symbol == 'R':
            piece = Rook(team, coord)
        elif symbol == 'B':
            piece = Bishop(team, coord)
        elif symbol == 'N':
            piece = Knight(team, coord)
        self.board_state.add_piece(piece, team, coord)
        return 

    def en_passant(self, to_coord: Coord, team: str) -> None:
        """
        Removes pawn captured by En passant
        to_coord: Coord, coordinate piece is moving to
        team: str, team of the pawn capturing
        """
        y_change = 1 if team == 'W' else -1
        enemy = 'W' if team == 'B' else 'B'
        x, y = to_coord
        self.board_state.remove_piece(Pawn(enemy, Coord(x, y - y_change)))
        return

    def left_in_check(self, board: Board) -> bool:
        """
        Returns True if own king was left in check, False otherwise
        board: Board, current board
        """
        enemy = 'W' if self.turn == 'B' else 'B'
        # Remember piece if taking
        to_x, to_y = self.to_coord
        piece_mem = board[to_x][to_y]
        if piece_mem:
            board.remove_piece(piece_mem)
            piece_pos = piece_mem.get_position()

        # Move piece
        board.move_piece(self.from_coord, self.to_coord, self.turn_number)
        board.switch_turns()

        # Check if left in check            
        result = board.in_check(self.turn_number, self.piece.get_team())

        # Move piece back
        board.move_piece(self.to_coord, self.from_coord, self.turn_number)
        board.switch_turns()
        
        # Replace missing piece
        if piece_mem:
            board.add_piece(piece_mem, enemy, piece_pos)
        board.update_all_sees(self.turn_number)
        return result
