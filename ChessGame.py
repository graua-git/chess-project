# Definition for a Chess Game class

from Move import Move
from Piece import Piece
from Coord import Coord
from StartingBoard import StartingBoard

#from Functions import *

class InvalidMoveError(Exception):
    pass

class ChessGame():
    def __init__(self, moves: str = None):
        self.board = StartingBoard().get_starting_board()
        self.turn = 'White'
        self.winner = None
        self.move_log = ''
        self.turn_number = 1
        self.update_piece_visibility()
        if moves is not None or moves != '':
            self._set_starting_position(moves)

    def __repr__(self):
        """
        Converts ChessGame into readable string
        """
        result = '--------------------------------------------------------------- \n'
        for y in reversed(range(8)):
            for x in range(8):
                result += str(self.board[x][y])
                result += ', '
            result += (' \n \n')
        return result + '---------------------------------------------------------------'
    
    # ------------------------------ Getters and Setters ------------------------------
    def _set_starting_position(self, moves: str) -> None:
        """
        Sets starting position for the board based on a series of legal moves
        moves: str representing a series of moves in chess notation
        returns: None, updates self.board
        """
        nums = '0123456789'
        move_list = moves.split('. ')
        move_list.remove('1')
        string_move_list = ''
        for i in range(len(move_list)):
            string_move_list += move_list[i] + ' '
        move_list = string_move_list.split(' ')
        result = []
        for move in move_list:
            if len(move) > 1:
                if move[0] not in nums:
                    result.append(move)
        for move in result:
            self.move(move)

    def _switch_turns(self):
        if self.turn == 'White':
            self.turn = 'Black'
        else:
            self.turn = 'White'
            self.turn_number += 1

    def get_material_difference(self):
        """
        Returns the difference in material value between Black and White
        Positive for White, negative for Black
        """
        result = 0
        for row in self.board:
            for square in row:
                if square is not None:
                    val = square.get_value()
                    if square.get_team() == 'Black':
                        val = -val
                else:
                    val = 0
                result += val
        return result

    def get_move_log(self):
        return self.move_log
    
    def _get_legal_moves(self, piece: Piece):
        """
        Returns list of coordinates to represent legal squares piece can move to
        piece: Piece to move
        """
        primary_legal_moves = piece.legal_moves(self.board)
        return primary_legal_moves
    
    def update_piece_visibility(self) -> None:
        """
        Updates which squares all pieces can see
        returns: None
        """
        for row in self.board:
            for piece in row:
                if piece is not None:
                    piece.update_sees(self.board)

    # --------------------------------- Move & Helper Functions ---------------------------------
    def move(self, notation: str) -> None:
        """
        Make a move on the chess board using chess notation
        notation: move in chess notation ex. e4, Nf3, Ke2, Bxf6, O-O
        """
        if len(notation) == 0:
            return
        move = Move(notation, self.turn, self.board)
        if move.castle:
            self.castle(move.castle)
        else:
            self._move_helper(move.from_coord, move.to_coord)

    def _move_helper(self, from_coord: Coord, to_coord: Coord) -> None:
        """
        Moves one piece from one square to another, if the move is legal
        from_coord: Tuple coordinates
        to_coord: Tuple coordinates
        return: None, alters chess board if move is legal, raises error otherwise
        """
        piece: Piece = self.board[from_coord.x][from_coord.y]
        
        # Check if it is a legal move
        legal_moves = self._get_legal_moves(piece)
        try:
            if to_coord not in legal_moves:
                raise InvalidMoveError
        except InvalidMoveError:
            print("Exception occured: Illegal move from {} to {}".format(piece, to_coord))
            return

        # Can start to make move
        takes = False  # True if a piece was captured in this move
        if self.board[to_coord.x][to_coord.y] is not None:
            takes = True
        check = False  # True if next opponent is in check

        # Move piece
        self._move_piece(piece, to_coord)

        # Append move to log
        self.append_move(piece, from_coord, takes, check, None)

        # Update piece visibility
        self.update_piece_visibility()

        # Update ability to castle, if necessary
        if piece.get_symbol() == 'K' or piece.get_symbol() == 'R':
            piece.set_castle() == False

        # Switch turns
        self._switch_turns()

    def _move_piece(self, piece: Piece, to_coord: Coord) -> None:
        """
        moves piece from from_coord to to_coord
        from_coord: Coordinate on chess board to represent starting position
        to_coord: Coordinate on chess board to represent ending position
        """
        from_coord = piece.get_position()
        piece.set_position(to_coord)
        self.board[from_coord.x][from_coord.y] = None
        self.board[to_coord.x][to_coord.y] = piece
        return

    def castle(self, side):
        """
        Castles king either to king side or queen side
        King moves two spaces over left or right and rook switches sides to protect the King
        The king cannot castle out of, into, or through check
        side: 'short' for king side castle, 'long' for queen side castle
        """
        # Get king and correct rook
        if self.turn == 'White':
            y = 0
        else:
            y = 7
        if side == 'short':
            rook_x = 7
            direction = 1
            rook_distance = 2
            notation = 'O-O'
            check_visiblity_squares = [4, 5, 6]
            check_empty_squares = [5, 6]
        else:
            rook_x = 0
            direction = -1
            rook_distance = 3
            notation = 'O-O-O'
            check_visiblity_squares = [4, 3, 2]
            check_empty_squares = [3, 2, 1]
        king: Piece = self.board[4][y]
        rook: Piece = self.board[rook_x][y]

        # If they cannot castle raise exception
        if king is None or rook is None:
            raise InvalidMoveError
        if not king.get_castle() or not rook.get_castle():
            raise InvalidMoveError
        
        # Check if squares are empty for king to castle
        for x in check_empty_squares:
            if self.board[x][y] is not None:
                raise InvalidMoveError
            
        # Check if king is castling into, out of, or through check
        for x in check_visiblity_squares:
            if self.turn == 'White':
                team = 'Black'
            else:
                team = 'White'
            if self._is_visible(Coord(x, y), team):
                raise InvalidMoveError

        # Move king and rook
        self._move_piece(king, Coord(king.get_position().x + (direction * 2), y))
        self._move_piece(rook, Coord(rook.get_position().x + (-direction * rook_distance), y))

        check = False
        # Append move to log
        self.append_move(king, None, False, check, notation)

        # Update piece visibility
        self.update_piece_visibility()

        # Switch turns
        self._switch_turns()

    def _is_visible(self, square: Coord, team: str) -> bool:
        """
        Returns true if the square is seen by a piece on team, false otherwise
        square: Coord representing square to check
        team: str 'Black' or 'White' of whos pieces to check
        """
        for col in self.board:
            for piece in col:
                if piece is not None:
                    if piece.get_team() == team:
                        if square in piece.get_sees():
                            return True
        return False

    def append_move(self, piece: Piece, from_coord: Coord, takes: bool, check: bool, castle: str) -> None:
        """
        Adds move to move_log
        piece: piece being moved
        from_coord: where the piece comes from
        takes: if the piece is taking another
        check: if the piece creates a check
        castle: 'short' or 'long' depending on the side of castle, None if False
        returns: None
        """
        symbol = piece.get_symbol()
        result = ''
        # Set new move if necessary
        if self.move_log != '':
            result += ' '
        if self.turn == 'White':
            result += str(self.turn_number) + '. '
        # Use castle notation if necessary
        if castle:
            result += castle
        # Create move notation
        else:
            if symbol != 'P':
                result += str(piece.get_symbol())
            

            if takes:
                if symbol == 'P':
                    result += str(from_coord)[0]
                result += 'x'

            result += str(piece.get_position())

        if check:
            result += '+'
        
        self.move_log += result

    def in_check(self):
        pass


if __name__ == '__main__':
    starting_pos = '1. e4 e5 2. Nf3 Nc6 3. d3 d6 4. Be3 Be7 5. Nc3 Nf6 6. Qd2 O-O 7. O-O-O d5 \
                    8. Nxd5 Nxd5 9. exd5 Nb4 10. d6 Bxd6 11. a3 Nc6 12. b4 h5 13. Nxe5 Bxe5 14. Qc3 Bxc3'
    game = ChessGame(starting_pos)
    print(game)
    print(game.get_move_log())
    print(game.get_material_difference())
