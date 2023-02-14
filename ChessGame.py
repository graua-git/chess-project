# Definition for a Chess Game class

from Move import *
from Piece import Piece
from Coord import Coord
from StartingBoard import StartingBoard

#from Functions import *

class ChessGame():
    def __init__(self, moves: str = None):
        self.board = StartingBoard().get_starting_board()
        self.turn = 'White'
        self.winner = None
        self.move_log = []
        self.turn_number = 1
        self.update_piece_visibility()
        if moves is not None and moves != '':
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
        # Filter out empty strings
        move_list = [move for move in move_list if len(move) > 1]
        # Filter out turn number notation
        move_list = [move for move in move_list if move[0] not in nums]
        for move in move_list:
            try:
                self.move(move)
            except InvalidMoveError:
                return

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

    def get_move_log(self) -> str:
        """
        Returns the list of moves in string format
        """
        result = ''
        for i, move in enumerate(self.move_log):
            if i % 2 == 0:
                turn_number = str(int(i / 2 + 1))
                result += turn_number + '. '
            result += str(move) + ' '
        return result
    
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
        if move.properties['castle']:
            self.castle(move)
        else:
            self._move_helper(move)

    def _move_helper(self, move: Move) -> None:
        """
        Moves one piece from one square to another, if the move is legal
        from_coord: Tuple coordinates
        to_coord: Tuple coordinates
        return: None, alters chess board if move is legal, raises error otherwise
        """
        from_coord, to_coord =  move.from_coord, move.to_coord
        piece: Piece = self.board[from_coord.x][from_coord.y]

        if self.board[to_coord.x][to_coord.y] is not None:
            move.properties['takes'] = True
        check = False  # True if next opponent is in check

        # Move piece
        self._move_piece(piece, to_coord)

        # Promote if necessary
        if move.properties['promotion']:
            symbol = move.promotion_piece
            piece._promote(symbol)

        # Append move to log
        self.move_log.append(move)

        # Update piece visibility
        self.update_piece_visibility()

        # Update ability to castle, if necessary
        if piece.get_symbol() == 'K' or piece.get_symbol() == 'R':
            piece.set_castle(False)

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

    def castle(self, move: Move):
        """
        Castles king either to king side or queen side
        King moves two spaces over left or right and rook switches sides to protect the King
        The king cannot castle out of, into, or through check
        move: move, castle either 'short' for king side castle, 'long' for queen side castle
        """
        # Get king and correct rook
        if self.turn == 'White':
            y = 0
        else:
            y = 7
        if move.get_castle_side() == 'short':
            rook_x = 7
            direction = 1
            rook_distance = 2
            check_visiblity_squares = [4, 5, 6]
            check_empty_squares = [5, 6]
        else:
            rook_x = 0
            direction = -1
            rook_distance = 3
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
        self.move_log.append(move)

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

    def in_check(self):
        pass


if __name__ == '__main__':
    starting_pos = '1. e4 c6 2. e5 d5 3. exd6 exd6 4. Qe2+ Qe7 5. Qxe7+ Bxe7 6. Nf3 Bg4 7. Be2 Nf6 8. d3 h6 9. O-O O-O 10. h3 Bh5 \
                        11. Nc3 Re8 12. Be3 c5 13. g4 Bg6 14. d4 cxd4 15. Nxd4 Nc6 16. Nxc6 bxc6 17. Rac1 Rab8 18. b3 d5 19. Bxa7 Ra8 20. Bd4 Ne4 \
                        21. Nxe4 Bxe4 22. a4 Ba3 23. Ra1 Bxc2 24. Rxa3 Rxe2 25. Ra2 Rae8 26. b4 Bb3 27. Rxe2 Rxe2 28. a5 Bc4 29. Bc5 Kh7 30. Kg2 Kg6 \
                        31. Kf3 Kg5 32. Rc1 Kh4 33. Rh1 d4 34. Be7+ g5 35. Bc5 Bd5+ 36. Kxe2 Bxh1 37. Bxd4 Kxh3 38. f3 Kg3 39. a6 Bxf3+ 40. Kd3 c5 \
                        41. Bxc5 Kxg4 42. b5 h5 43. b6 h4 44. a7 h3 45. b7 Bxb7 46. Bg1 Kg3 47. Ke2 Kg2 48. Bc5 h2 49. Bd6 h1=Q 50. Kd3 Qf1+ \
                        51. Kd4 Qf6+ 52. Kc5 Qf5+ 53. Kb6 Qe6 54. Kxb7 Qd7+ 55. Bc7 Qe7 56. a8=Q Qe4+ 57. Kc8 Qxa8+'
    game = ChessGame(starting_pos)
    print(game)
    print(game.get_move_log())
    print(game.get_material_difference())