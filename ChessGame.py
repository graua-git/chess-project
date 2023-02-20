from Board import *
from Move import *
import copy

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
        # Verify move
        turn = self.board.get_turn()
        try:
            curr_move = Move(self.board, turn, self.get_turn_number(), move)
        except InvalidMoveError:
            return

        self.move_log.append(curr_move)
        self.num_moves += 1
        self.board = copy.deepcopy(curr_move.get_board_state())
    
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
        '1. e4 c6 2. e5 d5 3. exd6 exd6 4. Qe2+ Qe7 5. Qxe7+ Bxe7 6. Nf3 Bg4 7. Be2 Nf6 8. d3 h6 9. O-O O-O 10. h3 Bh5 \
        11. Nc3 Re8 12. Be3 c5 13. g4 Bg6 14. d4 cxd4 15. Nxd4 Nc6 16. Nxc6 bxc6 17. Rac1 Rab8 18. b3 d5 19. Bxa7 Ra8 20. Bd4 Ne4 \
        21. Nxe4 Bxe4 22. a4 Ba3 23. Ra1 Bxc2 24. Rxa3 Rxe2 25. Ra2 Rae8 26. b4 Bb3 27. Rxe2 Rxe2 28. a5 Bc4 29. Bc5 Kh7 30. Kg2 Kg6 \
        31. Kf3 Kg5 32. Rc1 Kh4 33. Rh1 d4 34. Be7+ g5 35. Bc5 Bd5+ 36. Kxe2 Bxh1 37. Bxd4 Kxh3 38. f3 Kg3 39. a6 Bxf3+ 40. Kd3 c5 \
        41. Bxc5 Kxg4 42. b5 h5 43. b6 h4 44. a7 h3 45. b7 Bxb7 46. Bg1 Kg3 47. Ke2 Kg2 48. Bc5 h2 49. Bd6 h1=Q 50. Kd3 Qf1+ \
        51. Kd4 Qf6+ 52. Kc5 Qf5+ 53. Kb6 Qe6 54. Kxb7 Qd7+ 55. Bc7 Qe7 56. a8=Q Qe4+ 57. Kc8 Qxa8+'
    """
    starting_pos = '1. e4 c6 2. e5 d5 3. exd6 exd6 4. Qe2+ Qe7 5. Qxe7+ Bxe7 6. Nf3 Bg4 7. Be2 Nf6 8. d3 h6 9. O-O O-O 10. h3 Bh5 \
                    11. Nc3 Re8 12. Be3 c5 13. g4 Bg6 14. d4 cxd4 15. Nxd4 Nc6 16. Nxc6 bxc6 17. Rac1 Rab8 18. b3 d5 19. Bxa7 Ra8 20. Bd4 Ne4 \
                    21. Nxe4 Bxe4 22. a4 Ba3 23. Ra1 Bxc2 24. Rxa3 Rxe2 25. Ra2 Rae8 26. b4 Bb3 27. Rxe2 Rxe2 28. a5 Bc4 29. Bc5 Kh7 30. Kg2 Kg6 \
                    31. Kf3 Kg5 32. Rc1 Kh4 33. Rh1 d4 34. Be7+ g5 35. Bc5 Bd5+ 36. Kxe2 Bxh1 37. Bxd4 Kxh3 38. f3 Kg3 39. a6 Bxf3+ 40. Kd3 c5 \
                    41. Bxc5 Kxg4 42. b5 h5 43. b6 h4 44. a7 h3 45. b7 Bxb7 46. Bg1 Kg3 47. Ke2 Kg2 48. Bc5 h2 49. Bd6 h1=Q 50. Kd3 Qf1+ \
                    51. Kd4 Qf6+ 52. Kc5 Qf5+ 53. Kb6 Qe6 54. Kxb7 Qd7+ 55. Bc7 Qe7 56. a8=Q Qe4+ 57. Kc8 Qxa8+'
    game = ChessGame(starting_pos)
    game.move('Kb7')
    print_all(game)