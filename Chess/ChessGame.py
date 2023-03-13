from Chess.Board import *
from Chess.Move import *
import copy

class GameOver(Exception):
    pass

class ChessGame:
    def __init__(self, starting_moves: str = None):
        """
        starting_moves: MoveLog to set the board to a certain position, optional
        """
        self.board = Board()
        self.move_log = []
        self.num_moves = 0
        self.winner = None

        self.board.update_all_sees(1)
        self.legal_moves = self.set_all_legal_moves()

        if starting_moves:
            self.set_log(starting_moves)

    def __repr__(self):
        return str(self.board)

    # ------------------------------------------- Getters -------------------------------------------
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
    
    def get_turn_number(self) -> int:
        """
        Returns current turn number
        """
        return self.move_log.get_turn_number()

    def get_turn(self) -> str:
        """
        Returns player to move
        """
        return self.board.get_turn()

    def get_winner(self) -> str:
        """
        Returns winner
        """
        return self.winner

    def get_material_difference(self) -> int:
        """
        Returns difference in material points, + for white, - for black
        """
        result = 0
        for white_piece in self.board.get_white_pieces():
            result += white_piece.get_value()
        for black_piece in self.board.get_black_pieces():
            result -= black_piece.get_value()
        return result
    
    def get_turn_number(self) -> int:
        """
        Returns current turn number
        """
        return int(self.num_moves / 2 + 1)
    
    def get_current_board(self) -> Board:
        """
        Returns the board state of the last move played
        """
        return self.board
    
    def get_all_legal_moves(self) -> list[Move]:
        """
        Returns list of all legal moves for the current state
        """
        return self.legal_moves
    
    def print_all(self) -> None:
        """
        Prints the board, move_log, and player to move for game
        """
        print(self)
        print("Valutation: ", self.get_material_difference())
        print("Move Log: ", self.get_move_log())
        if not self.get_winner():
            print(self.get_turn() + " to move...")

    # ------------------------------------------- Setters -------------------------------------------
    def set_log(self, log: str) -> None:
        """
        Converts string move log into list and plays each move
        """
        nums = '0123456789'
        result = []
        
        # Split string to get move notations
        move_list = log.split('. ')
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
                break
        return result
    
    def set_all_legal_moves(self) -> list[Move]:
        """
        Returns list of all legal moves for player
        """
        result = []
        to_move = self.board.get_turn()
        turn_number = self.get_turn_number()
        piece_list = self.board.get_white_pieces() if to_move == 'W' else self.board.get_black_pieces()

        for piece in piece_list:
            from_coord = piece.get_position()
            for to_coord in piece.get_sees(self.board, turn_number):
                try:
                    curr_move = Move(self.board, to_move, turn_number, from_coord, to_coord)
                    if self.promotion_move(piece, to_coord):
                        pieces = ['Q', 'R', 'B', 'N']
                        for upgrade in pieces:
                            promotion_move = copy.deepcopy(curr_move)
                            promotion_move.properties['promotion'] = True
                            promotion_move.set_promotion_piece(upgrade)
                            result.append(promotion_move)
                        continue
                except InvalidMoveError:
                    continue
                result.append(curr_move)
        return result

    # ------------------------------------------- Move -------------------------------------------
    def move(self, move):
        """
        Makes move, updating board and move log
        """
        potential_moves = self.get_all_legal_moves()

        if len(potential_moves) == 0 or self.get_turn_number() > 100:
            self.end_game('turns')
            return
        
        # Verify move
        if move in potential_moves:
            curr_move = potential_moves[potential_moves.index(move)]
        else:
            return

        curr_move.commit_move()
        self.move_log.append(curr_move)
        self.num_moves += 1
        self.board = copy.deepcopy(curr_move.get_board_state())
        self.board.update_all_sees(self.get_turn_number())
        self.legal_moves = self.set_all_legal_moves()
        if len(self.legal_moves) == 0:
            self.end_game('moves')
            return
    
    def end_game(self, cause: str) -> None:
        """
        Ends game
        cause: str, 'turns' if too many moves have been played
        """
        if cause == 'turns':
            self.winner = 'D'
            return
        
        team = self.get_turn()
        if self.board.in_check(self.get_turn_number(), team):
            self.winner = 'W' if team == 'B' else 'B'
        else:
            self.winner = 'D'
        return
            
    def promotion_move(self, piece: Piece, to_coord: Coord) -> bool:
        """
        Returns true if pawn should promote this move, false otherwise
        piece: Piece, pawn in question
        to_coord: Coord, coordinate pawn is moving to
        """
        if isinstance(piece, Pawn):
            y = to_coord.y()
            team = piece.get_team()
            return (y == 7 and team == 'W') or (y == 0 and team == 'B')
        return False
