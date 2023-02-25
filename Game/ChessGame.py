from Board import *
from Move import *
import copy
import time

total_time = 0
num_moves = 0

def timer(func):
    def wrapper(*args, **kwargs):
        global total_time, num_moves
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        total_time += t2 - t1
        num_moves += 1
        print("Avg time: {}".format(total_time / num_moves))
    return wrapper

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
        return: current turn number
        """
        return self.move_log.get_turn_number()

    def get_turn(self) -> str:
        """
        return: player to move
        """
        return self.board.get_turn()

    def get_winner(self) -> str:
        """
        return: winner
        """
        return self.winner

    def get_material_difference(self) -> int:
        """
        return: difference in material points, + for white, - for black
        """
        result = 0
        for white_piece in self.board.get_white_pieces():
            result += white_piece.get_value()
        for black_piece in self.board.get_black_pieces():
            result -= black_piece.get_value()
        return result
    
    def get_turn_number(self) -> int:
        """
        return: current turn number
        """
        return int(self.num_moves / 2 + 1)
    
    def get_current_board(self) -> Board:
        """
        Returns the board state of the last move played
        """
        return self.board
    
    def get_all_legal_moves(self) -> list[Move]:
        """
        Returns all legal moves
        """
        return self.legal_moves

    # ------------------------------------------- Setters -------------------------------------------
    def set_log(self, log: str) -> None:
        """
        Converts string move log into list
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
    
    def end_game(self, cause: str):
        """
        Ends game
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
        if isinstance(piece, Pawn):
            y = to_coord.y()
            team = piece.get_team()
            return (y == 7 and team == 'W') or (y == 0 and team == 'B')
        return False


def print_all(game: ChessGame) -> None:
    """
    Prints the board, move_log, and player to move for game
    """
    print(game)
    print("Valutation: ", game.get_material_difference())
    print("Move Log: ", game.get_move_log())
    if not game.get_winner():
        print(game.get_turn() + " to move...")

if __name__ == '__main__':
    starting_position = '1. e3 e5 2. Bb5 Qh4 3. Bxd7 Bxd7 4. g4 Qxg4 5. Qxg4 Bxg4 6. f3 Bxf3 7. Nxf3 Nc6 8. Nxe5 Nxe5 9. b4 Bxb4 10. Nc3 Bxc3 11. dxc3 Rd8 12. Ba3 Rd6 13. Bxd6 \
                        cxd6 14. h4 Ne7 15. h5 Kd7 16. a4 Rc8 17. c4 Rxc4 18. e4 Rxc2 19. a5'
    game = ChessGame(starting_position)
    game.move('Nf3')
    print_all(game)
    print(game.get_all_legal_moves())
    """
    while not game.get_winner():
        print_all(game)
        print(game.get_all_legal_moves())
        move = input("Next Move: ")
        if move.lower() == 'stop' or move.lower() == 'kill':
            break
        game.move(move)
    print_all(game)
    print("Result: ", game.get_winner())
    print(game.get_avg_move_time())
    """