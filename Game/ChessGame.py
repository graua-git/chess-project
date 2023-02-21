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
        board = Board()
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
        turn = self.board.get_turn()
        #self.check_game_over(turn)

        if self.winner:
            raise GameOver
        
        # Verify move
        try:
            curr_move = Move(self.board, turn, self.get_turn_number(), move)
        except InvalidMoveError:
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
                        curr_move = Move(self.board, to_move, turn_number, (from_coord, to_coord))
                    except InvalidMoveError:
                        continue
                    result.append(curr_move)
        return result
    
    def check_game_over(self, team: str) -> None:
        """
        Sets self.winner to 'W' 'B' or 'D' for draw 
        """
        if len(self.get_all_legal_moves()) == 0:
            return


def print_all(game: ChessGame) -> None:
    """
    Prints the board, move_log, and player to move for game
    """
    print(game)
    print("Valutation: ", game.get_material_difference())
    print("Move Log: ", game.get_move_log())
    print(game.get_turn() + " to move...")

if __name__ == '__main__':
    """
        '1. c4 c5 2. Nc3 Nc6 3. g3 g6 4. Bg2 Bg7 5. e3 Nf6 6. Nge2 O-O 7. O-O Qb6 8. b3 d6 9. d4 Bg4 10. f3 Bd7 \
        11. Bb2 cxd4 12. Nxd4 e5 13. Nxc6 Bxc6 14. Na4 Qxe3+ 15. Kh1 Bxa4 16. bxa4 Rac8 17. Rc1 Qb6 18. Ba3 Rc6 19. f4 exf4 20. Bxc6 Qxc6+ \
        21. Qf3 Qb6 22. Qxf4 Nh5 23. Qxd6 Qe3 24. Rfe1 Qf3+ 25. Kg1 Nxg3 26. Qxg3 Bd4+ 27. Qf2 Be3 28. Rxe3 Qxf2+ 29. Kxf2'
    """
    starting_pos = '1. c4 c5 2. Nc3 Nc6 3. g3 g6 4. Bg2 Bg7 5. e3 Nf6 6. Nge2 O-O 7. O-O Qb6 8. b3 d6 9. d4 Bg4 10. f3 Bd7 \
        11. Bb2 cxd4 12. Nxd4 e5 13. Nxc6 Bxc6 14. Na4 Qxe3+ 15. Kh1 Bxa4 16. bxa4 Rac8 17. Rc1 Qb6 18. Ba3 Rc6 19. f4 exf4 20. Bxc6 Qxc6+ \
        21. Qf3 Qb6 22. Qxf4 Nh5 23. Qxd6 Qe3 24. Rfe1 Qf3+ 25. Kg1 Nxg3 26. Qxg3 Bd4+ 27. Qf2 Be3 28. Rxe3 Qxf2+'
    game = ChessGame(starting_pos)
    print_all(game)
    print(game.get_all_legal_moves())