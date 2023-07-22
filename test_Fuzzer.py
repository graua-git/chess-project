import unittest
import random
import time
from Chess.ChessGame import *

PIECES = ['P', 'N', 'B', 'R', 'Q', 'K']
LETTERS = 'abcdefgh'
NUMBERS = '12345678'


class Fuzzer(unittest.TestCase):
    def test(self):
        # Generation-based fuzzer to throw random moves at the game
        # Chosen using Random Testing
        tests = 1
        winners = {'W': 0, 'B': 0, 'D': 0}
        for i in range(tests):
            game = ChessGame()
            t1 = time.time()
            while game.get_winner() is None:
                move = self.generate_move()
                game.move(move)
            t2 = time.time()
            total_time = round(t2 - t1, 3)
            time_per_move = total_time / game.num_moves
            game.print_all()
            print(f"Game {i+1} ran in {total_time}s. Time/Move: {round(time_per_move * 1000, 2)}ms")
            winners[game.get_winner()] += 1
        print('Data: ' + str(winners))
    
    def generate_move(self):
        # Generates move to perform in game

        # Castles
        if random.randint(1, 50) == 1:
            return 'O-O'
        elif random.randint(1, 50) == 1:
            return 'O-O-O'

        # Get piece to move
        piece = random.choice(PIECES)
        to_coord = str(Coord(random.randint(0, 7), random.randint(0, 7)))

        # Takes odds 1 / 2
        takes = ''
        if random.randint(1, 2) == 1:
            takes = 'x'
        
        promotion = ''
        extra = ''
        if piece == 'P':
            piece = ''
            if takes:
                extra = random.choice(LETTERS)
            if random.randint(1, 5) == 1:
                promotion = '=' + random.choice(PIECES)
        if piece == 'N' or piece == 'R' or piece == 'Q':
            if random.randint(1, 10) == 1:
                if random.randint(1, 2) == 1:
                    extra = random.choice(LETTERS)
                else:
                    extra = random.choice(NUMBERS)

        return piece + extra + takes + to_coord + promotion

if __name__ == '__main__':
    unittest.main(verbosity=2)
