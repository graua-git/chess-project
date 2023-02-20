import unittest
from Piece import *

w, b = 'W', 'B'

board = [
    [Rook(w, Coord(0, 0)), None, Pawn(w, Coord(0, 2)), Pawn(b, Coord(0, 3)), None, None, None, Rook(b, Coord(0, 7))],
    [None, None, None, Pawn(w, Coord(1, 3)), None, Bishop(b, Coord(1, 5)), Pawn(b, Coord(1, 6)), None],
    [None, None, None, Pawn(w, Coord(2, 3)), Knight(w, Coord(2, 4)), Knight(b, Coord(2, 5)), Pawn(b, Coord(2, 6)), None],
    [None, None, Pawn(w, Coord(3, 2)), Pawn(b, Coord(3, 3)), None, None, None, Queen(b, Coord(3, 7))],
    [King(w, Coord(4, 0)), Bishop(w, Coord(4, 1)), None, None, None, None, None, King(b, Coord(4, 7))],
    [Rook(w, Coord(5, 0)), None, None, None, None, Knight(b, Coord(5, 5)), None, None],
    [None, Pawn(w, Coord(6, 1)), None, Queen(w, Coord(6, 3)), Bishop(w, Coord(6, 4)), Bishop(b, Coord(6, 5)), Pawn(b, Coord(6, 6)), None],
    [None, Pawn(w, Coord(7, 1)), Knight(w, Coord(7, 2)), None, None, None, Pawn(b, Coord(7, 6)), Rook(b, Coord(7, 7))]
]
turn_number = 14
pawn: Pawn = board[1][3]
pawn.en_passant = 13
pawn: Pawn = board[2][3]
pawn.en_passant = 12
rook: Rook = board[7][7]
rook._castle = False


class PieceVisionTestCase(unittest.TestCase):
    def test_pawn_1(self):
        pawn: Pawn = board[0][2]
        result = pawn.sees(board, turn_number)
        expected = []
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))
        
if __name__ == '__main__':
    unittest.main(verbosity=2)