

from Chess.ChessGame import *
from Chess.Move import *
from Chess.Board import *
import random
import copy

class Profile:
    def __init__(self, team):
        self.team = team

    def __repr__(self):
        return str(self.__name__)
    
    def get_move(self, game):
        self.pick_move(game)


class Player(Profile):
    def __init__(self, team):
        self.team = team

    def pick_move(self, game: ChessGame) -> str:
        """
        Player is controlled by the user, taking input to pick a move
        """
        return input("Your move: ")


class Kevin(Profile):
    def __init__(self, team: str):
        Profile.__init__(self, team)

    def pick_move(self, game: ChessGame) -> Move:
        """
        Kevin picks a legal move at random
        """
        move_list = game.get_legal_moves()
        return random.choice(move_list)


class Caleb(Profile):
    def __init__(self, team: str):
        Profile.__init__(self, team)

    def pick_move(self, game: ChessGame) -> Move:
        """
        Caleb will take pieces whenever possible
        """
        move_list = game.get_legal_moves()
        taking_moves = [move for move in move_list if 'x' in str(move)]
        if len(taking_moves) > 0:
            return random.choice(taking_moves)
        return random.choice(move_list)


class Nick(Profile):
    def __init__(self, team: str):
        Profile.__init__(self, team)

    def pick_move(self, game: ChessGame) -> Move:
        """
        Nick sees the value of his pieces, making sure they all see as many squares as possible
        """
        h_game = copy.deepcopy(game)
        move_list = h_game.get_legal_moves()
        taking_moves = [move for move in move_list if 'x' in str(move)]
        considered_moves = taking_moves if len(taking_moves) > 0 else move_list

        champs = [(None, 0)]
        for move in considered_moves:
            turn_number = game.get_turn_number()
            h_board = copy.deepcopy(h_game.get_current_board())
            # Make move
            move.set_board(h_board)
            move.commit_move()
            h_board.update_all_sees(turn_number)
            
            total_sees = self.get_total_sees(h_board, turn_number)
            if total_sees > champs[0][1]:
                champs = [(move, total_sees)]
            elif total_sees == champs[0][1]:
                champs.append((move, total_sees))
        picked_move = random.choice(champs)[0]
        picked_move.set_board(game.get_current_board())
        return picked_move

    def get_total_sees(self, board: Board, turn_number: int) -> int:
        total_sees = 0
        for row in board:
            for piece in row:
                if not piece:
                    continue
                if piece.get_team() != self.team:
                    continue
                sees = piece.get_sees(board, turn_number)
                total_sees += len(sees)
        return total_sees


class Luke(Profile):
    def __init__(self, team: str, **kwargs):
        Profile.__init__(self, team)
        self.multipliers = {
            'piece': -0.5,
            'sees': .1,
            'opponent moves': -.5,
            'material difference': 3
        }
        for key, value in kwargs.items():
            self.mulitpliers[key] = value
    
    def pick_move(self, game: ChessGame) -> Move:
        """
        Luke evaluates the board in its current position, picking a move to improve it
        """
        move_list = game.get_legal_moves()

        move_data_list = []
        champs = [{'eval': -1000}]
        for move in move_list:
            turn_number = game.get_turn_number()
            h_game = copy.deepcopy(game)
            # Make move
            h_game.move(move)
            move_data = self.get_data(move, h_game, h_game.get_current_board(), turn_number)
            move_data_list.append(move_data)
            if move_data['eval'] > champs[0]['eval']:
                champs = [move_data]
            elif move_data['eval'] == champs[0]['eval']:
                champs.append(move_data)

        choice = random.choice(champs)
        return choice['move']
        
    def get_data(self, move: Move, game: ChessGame, board: Board, turn_number: int) -> dict:
        """
        Gets data to evaluate next move
        """
        result = {
            'move': move,
            'piece': move.get_piece().get_value(),
            'sees': 0,
            'opponent moves': 0,
            'material difference': 0,
            'eval': 0
        }
        for row in board:
            for piece in row:
                if not piece:
                    continue
                if piece.get_team() != self.team:
                    sees = piece.get_sees(board, turn_number)
                    result['sees'] -= len(sees)
                    result['material difference'] -= piece.get_value()
                else:
                    sees = piece.get_sees(board, turn_number)
                    result['sees'] += len(sees)
                    result['material difference'] += piece.get_value()
        result['opponent moves'] = len(game.get_legal_moves())
        
        result['eval'] += result['piece'] * self.multipliers['piece']
        result['eval'] += result['sees'] * self.multipliers['sees']
        result['eval'] += result['opponent moves'] * self.multipliers['opponent moves']
        result['eval'] += result['material difference'] * self.multipliers['material difference']
        return result
