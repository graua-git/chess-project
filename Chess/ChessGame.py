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
        self.last_pawn_move = 0

        self.board.update_all_sees(1)
        self.legal_moves = self.find_legal_moves()

        if starting_moves:
            self.set_log(starting_moves)

    def __repr__(self):
        return str(self.board)
    
    def move_log_toJSON(self):
        result = []
        for i in range(0, int(len(self.move_log)), 2):
            move = []
            move.append(str(self.move_log[i]))
            if i + 1 < len(self.move_log):
                move.append(str(self.move_log[i + 1]))
            result.append(move)
        return json.dumps(result)

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
    
    def get_move_log_list(self) -> list:
        """
        Returns the list of moves in list format
        """
        return self.move_log
    
    def get_num_moves(self) -> int:
        """
        Returns number of moves played
        """
        return self.num_moves

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
        return self.get_total_material_value('W') - self.get_total_material_value('B')
    
    def get_total_material_value(self, team: str) -> int:
        """
        Returns material points of team's pieces
        team: str, 'W' or 'B'
        """
        result = 0
        piece_list = self.board.get_white_pieces() if team == 'W' else self.board.get_black_pieces()
        for piece in piece_list:
            result += piece.get_value()
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
    
    def get_legal_moves(self) -> list[Move]:
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
    
    def find_legal_moves(self, move: str = None) -> list[Move]:
        """
        Returns list of all legal moves for player
        move: str, if move is passed as argument, return Move if it's a legal move, None otherwise
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
                            if promotion_move == move:
                                promotion_move
                        continue
                except InvalidMoveError:
                    continue
                result.append(curr_move)
                if curr_move == move:
                    return curr_move
        if move is None:
            return result
        return None

    # ------------------------------------------- Move -------------------------------------------
    def move(self, move):
        """
        Makes move, updating board and move log
        """
        potential_moves = self.get_legal_moves()
        
        # Verify move
        if move in potential_moves:
            curr_move = potential_moves[potential_moves.index(move)]
        else:
            return

        curr_move.commit_move()
        self.move_log.append(curr_move)
        self.num_moves += 1
        self.board = curr_move.get_board_state()
        self.board.update_all_sees(self.get_turn_number())
        self.legal_moves = self.find_legal_moves()

        # Check for end game

        # Checkmate / Stalemate
        if len(self.legal_moves) == 0:
            self.end_game('moves')
            return
        
        # Insufficient Material 
        if self.insufficient_material():
            self.end_game('material')
            return

        # 50 Move rule
        if curr_move.get_piece().get_name() != 'Pawn':
            self.last_pawn_move += 1
        else:
            self.last_pawn_move = 0
        if self.last_pawn_move > 50:
            self.end_game('turns')
            return

    def end_game(self, cause: str) -> None:
        """
        Ends game
        cause: str, 'turns' if too many moves have been played
        """
        if cause == 'turns' or cause == 'material':
            self.winner = 'D'
            return

        team = self.get_turn()
        if self.board.in_check(self.get_turn_number(), team):
            self.winner = 'W' if team == 'B' else 'B'
        else:
            self.winner = 'D'
        return

    def insufficient_material(self) -> bool:
        """
        Returns True if the game is over by insufficient material, False otherise
        """
        white_material = self.get_total_material_value('W')
        black_material = self.get_total_material_value('B')
        white_insufficient = white_material == 100 or white_material == 103
        black_insufficient = black_material == 100 or black_material == 103
        return white_insufficient and black_insufficient
   
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
