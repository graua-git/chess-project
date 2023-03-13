import unittest
from Chess.Piece import *
from Chess.Board import *

w, b = 'W', 'B'
BOARD_1 = [
        [Rook(w, Coord(0, 0)), None, Pawn(w, Coord(0, 2)), Pawn(b, Coord(0, 3)), None, None, None, Rook(b, Coord(0, 7))],
        [None, None, None, Pawn(w, Coord(1, 3)), None, Bishop(b, Coord(1, 5)), Pawn(b, Coord(1, 6)), None],
        [None, None, None, Pawn(w, Coord(2, 3)), Knight(w, Coord(2, 4)), Knight(b, Coord(2, 5)), Pawn(b, Coord(2, 6)), None],
        [None, None, Pawn(w, Coord(3, 2)), Pawn(b, Coord(3, 3)), None, None, None, Queen(b, Coord(3, 7))],
        [King(w, Coord(4, 0)), Bishop(w, Coord(4, 1)), None, Queen(w, Coord(4, 3)), None, Pawn(b, Coord(4, 5)), None, King(b, Coord(4, 7))],
        [Rook(w, Coord(5, 0)), None, None, None, None, Knight(b, Coord(5, 5)), None, None],
        [None, Pawn(w, Coord(6, 1)), None, None, Bishop(w, Coord(6, 4)), Bishop(b, Coord(6, 5)), Pawn(b, Coord(6, 6)), None],
        [None, Pawn(w, Coord(7, 1)), None, Knight(w, Coord(7, 3)), None, Pawn(b, Coord(7, 5)), None, Rook(b, Coord(7, 7))]
    ]

TURN_NUMBER_1 = 14
pawn: Pawn = BOARD_1[1][3]
pawn.set_en_passant(14)
pawn: Pawn = BOARD_1[2][3]
pawn.set_en_passant(13)
rook: Rook = BOARD_1[7][7]
rook.set_castle(False)

b1 = Board(BOARD_1)
b1.update_all_sees(TURN_NUMBER_1)

class PieceVisionTestCase(unittest.TestCase):
    # ------------------------------------------------ Pawns ------------------------------------------------
    def test_pawn_1(self):
        # White Pawn on a3
        pawn: Pawn = BOARD_1[0][2]
        result = pawn.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = []
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))
    
    def test_pawn_2(self):
        # White Pawn on b4
        pawn: Pawn = BOARD_1[1][3]
        result = pawn.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = ['b5']
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    def test_pawn_3(self):
        # White Pawn on c4
        pawn: Pawn = BOARD_1[2][3]
        result = pawn.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = []
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))
    
    def test_pawn_4(self):
        # White Pawn on d3
        pawn: Pawn = BOARD_1[3][2]
        result = pawn.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = []
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    def test_pawn_5(self):
        # White Pawn on g2
        pawn: Pawn = BOARD_1[6][1]
        result = pawn.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = ['g3', 'g4']
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    def test_pawn_6(self):
        # White Pawn on d3
        pawn: Pawn = BOARD_1[7][1]
        result = pawn.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = ['h3']
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    def test_pawn_7(self):
        # Black Pawn on a4
        pawn: Pawn = BOARD_1[0][3]
        result = pawn.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = ['b3']
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    def test_pawn_8(self):
        # Black Pawn on b7
        pawn: Pawn = BOARD_1[1][6]
        result = pawn.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = []
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    def test_pawn_9(self):
        # Black Pawn on a4
        pawn: Pawn = BOARD_1[2][6]
        result = pawn.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = []
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    def test_pawn_10(self):
        # Black Pawn on d4
        pawn: Pawn = BOARD_1[3][2]
        result = pawn.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = []
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    def test_pawn_11(self):
        # Black Pawn on e6
        pawn: Pawn = BOARD_1[4][5]
        result = pawn.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = ['e5']
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))
    
    def test_pawn_12(self):
        # Black Pawn on g7
        pawn: Pawn = BOARD_1[6][6]
        result = pawn.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = []
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    def test_pawn_13(self):
        # Black Pawn on a4
        pawn: Pawn = BOARD_1[7][5]
        result = pawn.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = ['g5', 'h5']
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    # ----------------------------------------------- Knights -----------------------------------------------
    def test_knight_1(self):
        # White Knight on c5
        knight: Knight = BOARD_1[2][4]
        result = knight.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = ['a6', 'a4', 'b7', 'b3', 'd7', 'e6']
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    def test_knight_2(self):
        # White Knight on h4
        knight: Knight = BOARD_1[7][3]
        result = knight.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = ['f5', 'f3', 'g6']
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    def test_knight_3(self):
        # Black Knight on c6
        knight: Knight = BOARD_1[2][5]
        result = knight.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = ['a7', 'a5', 'b8', 'b4', 'e7', 'e5']
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    def test_knight_4(self):
        # Black Knight on f6
        knight: Knight = BOARD_1[5][5]
        result = knight.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = ['d7', 'd5', 'e4', 'g8', 'g4', 'h7', 'h5']
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    # ----------------------------------------------- Bishops -----------------------------------------------
    def test_bishop_1(self):
        # White Bishop on e2
        bishop: Bishop = BOARD_1[4][1]
        result = bishop.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = ['d1', 'f3', 'g4', 'h5']
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    def test_bishop_2(self):
        # White Bishop on g5
        bishop: Bishop = BOARD_1[6][4]
        result = bishop.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = ['f6', 'h6', 'f4', 'e3', 'd2', 'c1']
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    def test_bishop_3(self):
        # Black Bishop on b6
        bishop: Bishop = BOARD_1[1][5]
        result = bishop.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = ['a7', 'a5', 'c5']
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    def test_bishop_4(self):
        # Black Bishop on g6
        bishop: Bishop = BOARD_1[6][5]
        result = bishop.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = ['f7', 'h7', 'f5', 'e4', 'h5']
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    # ------------------------------------------------ Rooks ------------------------------------------------
    def test_rook_1(self):
        # White Rook on a1
        rook: Rook = BOARD_1[0][0]
        result = rook.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = ['a2', 'b1', 'c1', 'd1']
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    def test_rook_2(self):
        # White Rook on f1
        rook: Rook = BOARD_1[5][0]
        result = rook.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = ['g1', 'h1', 'f2', 'f3', 'f4', 'f5', 'f6']
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    def test_rook_3(self):
        # Black Rook on a8
        rook: Rook = BOARD_1[0][7]
        result = rook.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = ['a7', 'a6', 'a5', 'b8', 'c8']
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    def test_rook_4(self):
        # Black Rook on h8
        rook: Rook = BOARD_1[7][7]
        result = rook.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = ['h7', 'g8', 'f8']
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    # ----------------------------------------------- Queens ------------------------------------------------
    def test_queen_1(self):
        # White Queen on e4
        queen: Queen = BOARD_1[4][3]
        result = queen.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = ['e5', 'e6', 'f5', 'g6', 'f4', 'g4', 'f3', 'e3', 'd4', 'd5', 'c6']
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    def test_queen_2(self):
        # Black Queen on d7
        queen: Queen = BOARD_1[3][7]
        result = queen.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = ['e7', 'd7', 'd6', 'd5', 'c8', 'b8']
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    # ------------------------------------------------ Kings ------------------------------------------------
    def test_king_1(self):
        # White King on e1
        king: King = BOARD_1[4][0]
        result = king.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = ['O-O-O', 'd1', 'd2', 'f2']
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))

    def test_king_2(self):
        # Black King on e8
        king: King = BOARD_1[4][7]
        result = king.get_sees(BOARD_1, TURN_NUMBER_1)
        expected = ['d7', 'e7', 'f7', 'f8']
        self.assertCountEqual(result, expected, msg="Expected: {}, Got: {}".format(expected, result))
        
if __name__ == '__main__':
    unittest.main(verbosity=2)