from Board import *
from Move import *
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
        for row in self.board:
            for square in row:
                if square is not None:
                    val = square.get_value()
                    if square.get_team() == 'B':
                        val = -val
                else:
                    val = 0
                result += val
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
        final_move = self._move_log[-1]
        return final_move.board_state()
    
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
            self.end_game()
        
        # Verify move
        if move in potential_moves:
            curr_move = potential_moves[potential_moves.index(move)]
        else:
            return

        curr_move.commit_move()
        self.move_log.append(curr_move)
        self.num_moves += 1
        self.board = copy.deepcopy(curr_move.get_board_state())
    
    def get_all_legal_moves(self) -> list[Move]:
        """
        Returns list of all legal moves for player
        """
        result = []
        to_move = self.board.get_turn()
        turn_number = self.get_turn_number()
        for row in self.board.get_board_state():
            for piece in row:
                if not piece:
                    continue
                if piece.get_team() != to_move:
                    continue
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
    
    def end_game(self):
        """
        Ends game
        """
        self.winner = 'D'
            
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
    print(game.get_turn() + " to move...")

if __name__ == '__main__':
    starting_position = '1. e4 e5 2. d4 exd4 3. c3 dxc3 4. Bc4 cxb2 5. Qa4'
    game = ChessGame(starting_position)
    while not game.get_winner():
        print_all(game)
        print(game.get_all_legal_moves())
        move = input("Next Move: ")
        if move.lower() == 'stop' or move.lower() == 'kill':
            break
        game.move(move)
    print_all(game)
    print("Result: ", game.get_winner())