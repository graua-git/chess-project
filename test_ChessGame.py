import unittest
import time
from Chess.ChessGame import *
from Chess.Board import *

class TestGame(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        moves = ''
        cls.game = ChessGame(moves)
        cls.material_difference = 0
        cls.winner = None
        cls.time_per_move = 1
    def test_mat_difference(self):
        result = self.game.get_material_difference()
        expected = self.material_difference
        self.assertEqual(result, expected, msg="Game expected material difference = {}, got {}".format(expected, result))
    def test_correct_winner(self):
        result = self.game.get_winner()
        expected = self.winner
        self.assertEqual(result, expected, msg="Game expected winner: {}, got {}".format(expected, result))
    def test_move_time(self):
        if self.game.get_num_moves() == 0:
            result = 0
        else:
            result = round(self.total_time / self.game.get_num_moves(), 3)
        expected = self.time_per_move
        print(f"Time per move: {result}ms")
        self.assertLess(result, expected)
        

class TestGame1(TestGame):
    # andrewmcleodnz vs Me
    @classmethod
    def setUpClass(cls):
        t1 = time.time()
        moves = '1. c4 c5 2. Nc3 Nc6 3. g3 g6 4. Bg2 Bg7 5. e3 Nf6 6. Nge2 O-O 7. O-O Qb6 8. b3 d6 9. d4 Bg4 10. f3 Bd7 \
                    11. Bb2 cxd4 12. Nxd4 e5 13. Nxc6 Bxc6 14. Na4 Qxe3 15. Kh1 Bxa4 16. bxa4 Rac8 17. Rc1 Qb6 18. Ba3 Rc6 19. f4 exf4 20. Bxc6 Qxc6 \
                    21. Qf3 Qb6 22. Qxf4 Nh5 23. Qxd6 Qe3 24. Rfe1 Qf3 25. Kg1 Nxg3 26. Qxg3 Bd4 27. Qf2 Be3 28. Rxe3 Qxf2 29. Kxf2'
        cls.game = ChessGame(moves)
        t2 = time.time()
        cls.material_difference = 7
        cls.winner = None
        cls.total_time = (t2 - t1) * 1000
        cls.time_per_move = 40

class TestGame2(TestGame):
    # Me vs GMswaggyp
    @classmethod
    def setUpClass(cls):
        t1 = time.time()
        moves = '1. e4 e5 2. Nc3 Bc5 3. Bc4 Nc6 4. Qg4 Qf6 5. Nd5 Qxf2 6. Kd1 Na5 7. Nh3 Qd4 8. d3 Nxc4 9. c3 Qxd3 10. Ke1 Nf6 \
                    11. Qxg7 d6 12. Nxf6 Ke7 13. Nd5 Kd7 14. Qxf7 Kc6 15. Nb4 Bxb4 16. Qd5 Qxd5 17. exd5 Kxd5 18. cxb4 Bxh3 19. gxh3 h5 20. b3 Kc6 \
                    21. bxc4 a5 22. b5 Kc5 23. Be3 Kxc4 24. Rc1 Kxb5 25. Rxc7 Ka6 26. Rf1 Rac8 27. Rff7 Rxc7 28. Rxc7 b6 29. Rc6 Rd8 30. Rxb6 Ka7 \
                    31. Rxd6 Kb7 32. Rxd8'
        cls.game = ChessGame(moves)
        t2 = time.time()
        cls.material_difference = 8
        cls.winner = None
        cls.total_time = (t2 - t1) * 1000
        cls.time_per_move = 35


class TestGame3(TestGame):
    # Me vs ManuSd1998
    @classmethod
    def setUpClass(cls):
        t1 = time.time()
        moves = '1. e4 e6 2. Nc3 Qf6 3. Nf3 d5 4. exd5 exd5 5. d3 c6 6. Be2 Bb4 7. O-O Bxc3 8. bxc3 Qxc3 9. Rb1 Ne7 10. Bb2 Qa5 \
                    11. Bxg7 Rg8 12. Bh6 Qxa2 13. Ne5 Be6 14. c4 Nd7 15. cxd5 Nxe5 16. dxe6 Qxe6 17. Rxb7 Qxh6 18. d4 Nd7 19. Bg4 Rd8 20. Re1 Rxg4 \
                    21. Qxg4 Qd6 22. Qg8 Nf8 23. Rexe7 Qxe7 24. Rxe7 Kxe7 25. Qg5 Ke8 26. Qe5 Ne6 27. Qh8 Ke7 28. Qxh7 Rxd4 29. g3 a5 30. Qb1 a4 \
                    31. Qa1 c5 32. f4 Kd6 33. Kg2 Nc7 34. h4 Nb5 35. Kh3 a3 36. h5 Rd3 37. h6 Kc6 38. h7 Rd8 39. Qf6 Kc7 40. Qxd8 Kxd8 \
                    41. h8=Q Kc7 42. Qe5 Kb6 43. Qa1 Ka5 44. g4 Ka4 45. g5 Nc3 46. f5 a2 47. g6 Ka3 48. gxf7 Na4 49. f8=Q Nb2 50. Qxc5 Ka4 \
                    51. Qc2 Ka3 52. Qcxb2 Ka4 53. Qaxa2'
        cls.game = ChessGame(moves)
        t2 = time.time()
        cls.material_difference = 19
        cls.winner = 'W'
        cls.total_time = (t2 - t1) * 1000
        cls.time_per_move = 30


class TestGame4(TestGame):
    # LaGuinze vs Me
    @classmethod
    def setUpClass(cls):
        t1 = time.time()
        moves = '1. e4 c6 2. e5 d5 3. exd6 exd6 4. Qe2 Qe7 5. Qxe7 Bxe7 6. Nf3 Bg4 7. Be2 Nf6 8. d3 h6 9. O-O O-O 10. h3 Bh5 \
                    11. Nc3 Re8 12. Be3 c5 13. g4 Bg6 14. d4 cxd4 15. Nxd4 Nc6 16. Nxc6 bxc6 17. Rac1 Rab8 18. b3 d5 19. Bxa7 Ra8 20. Bd4 Ne4 \
                    21. Nxe4 Bxe4 22. a4 Ba3 23. Ra1 Bxc2 24. Rxa3 Rxe2 25. Ra2 Rae8 26. b4 Bb3 27. Rxe2 Rxe2 28. a5 Bc4 29. Bc5 Kh7 30. Kg2 Kg6 \
                    31. Kf3 Kg5 32. Rc1 Kh4 33. Rh1 d4 34. Be7 g5 35. Bc5 Bd5 36. Kxe2 Bxh1 37. Bxd4 Kxh3 38. f3 Kg3 39. a6 Bxf3 40. Kd3 c5 \
                    41. Bxc5 Kxg4 42. b5 h5 43. b6 h4 44. a7 h3 45. b7 Bxb7 46. Bg1 Kg3 47. Ke2 Kg2 48. Bc5 h2 49. Bd6 h1=Q 50. Kd3 Qf1 \
                    51. Kd4 Qf6 52. Kc5 Qf5 53. Kb6 Qe6 54. Kxb7 Qd7 55. Bc7 Qe7 56. a8=Q Qe4 57. Kc8 Qxa8'
        cls.game = ChessGame(moves)
        t2 = time.time()
        cls.material_difference = -8
        cls.winner = None
        cls.total_time = (t2 - t1) * 1000
        cls.time_per_move = 25


class TestGame5(TestGame):
    # alterfiend vs Me
    @classmethod
    def setUpClass(cls):
        t1 = time.time()
        moves = '1. e4 c6 2. Nf3 d5 3. Nc3 Bg4 4. exd5 cxd5 5. h3 Bxf3 6. Qxf3 e6 7. Bb5 Nc6 8. O-O Nf6 9. d4 a6 10. Ba4 b5 \
                    11. Bb3 Nxd4 12. Qg3 g6 13. Qe5 Nxb3 14. axb3 Bg7 15. Bg5 h6 16. Bh4 g5 17. Bg3 O-O 18. h4 Ne4 19. Qc7 Nxg3 20. Qxd8 Rfxd8 \
                    21. fxg3 Rac8 22. Rf3 Bd4 23. Kh2 f5 24. Rxa6 g4 25. Rd3 Bg7 26. Rxe6 Ra8 27. Rxd5 Rxd5 28. Nxd5 Bxb2 29. Rg6 Kh7 30. Rb6 Ra5 \
                    31. Nc7 b4 32. Rxb4 Bc3 33. Ra4 Rc5 34. Ne6 Re5 35. Nf4 Bd2 36. c4 Re3 37. Ra7 Kg8 38. c5 Be1 39. Nh5 Rxb3 40. c6 Rc3 \
                    41. c7 Bf2 42. Nf4 Bxa7 43. Nd5 Rc5 44. Ne7 Kf7 45. c8=Q Rxc8 46. Nxc8 Kf6 47. Nxa7 Ke5 48. Nc6 Kd6 49. Nd4 Ke5 50. Ne2 Ke4 \
                    51. Nf4 Ke5 52. Kg1 Kf6 53. Kf2 Ke5 54. Ke3 h5 55. Nxh5 Ke6 56. Kf4 Kf7 57. Kxf5 Ke7 58. Kxg4 Kf7 59. Nf4 Kg7 60. h5 Kh6 \
                    61. Kh4 Kg7 62. g4 Kh8 63. g5 Kg8 64. h6 Kf7 65. Kh5 Kg8 66. Ne6 Kh8 67. Nf4 Kg8 68. Ne6'
        cls.game = ChessGame(moves)
        t2 = time.time()
        cls.material_difference = 6
        cls.winner = None
        cls.total_time = (t2 - t1) * 1000
        cls.time_per_move = 25


class TestGame6(TestGame):
    # alterfiend vs Me
    @classmethod
    def setUpClass(cls):
        t1 = time.time()
        moves = '1. e4 e5 2. Nc3 Nf6 3. f4 d6 4. Nf3 Nc6 5. Bc4 Qe7 6. O-O Be6 7. Bb3 Bxb3 8. axb3 h6 9. d3 g5 10. fxe5 Nxe5 \
                    11. Nxe5 dxe5 12. Qf3 O-O-O 13. Be3 Kb8 14. Qxf6 Qxf6 15. Rxf6 Be7 16. Bxa7 Ka8 17. Bc5 Kb8 18. Bxe7 Rd7 19. Bc5 b6 20. Be3 g4 \
                    21. Nd5 h5 22. Nxb6 Rdd8 23. c3 cxb6 24. Rxb6 Kc7 25. Ra7 Kc8 26. Ra8 Kc7 27. Rxd8 Rxd8 28. Rf6 Rxd3 29. Rxf7 Kd8 30. Bb6 Ke8 \
                    31. Rf5 Rd2 32. Rxe5 Kd7 33. Rxh5 Rxb2 34. Bd4 Rxb3 35. Rg5 Rb1 36. Kf2 Rb2 37. Kg3 Re2 38. e5 Rd2 39. Rxg4 Rc2 40. h4 Ra2 \
                    41. h5 Ra8 42. h6 Rh8 43. Rg7 Kc6 44. h7 Kd5 45. Kh4 Ke4 46. Kg5 Kd5 47. Kf6 Kc6 48. g4 Kd5 49. g5 Kc6 50. g6 Kd5 \
                    51. Rd7 Ke4 52. g7 Rxh7 53. g8=Q Rh6 54. Qg6 Rxg6 55. Kxg6 Kf4 56. e6 Ke4 57. e7 Kd3 58. e8=Q Kc2 59. Qe2 Kb3 60. Rb7 Ka3 \
                    61. Qb2 Ka4 62. Qb4'
        cls.game = ChessGame(moves)
        t2 = time.time()
        cls.material_difference = 18
        cls.winner = 'W'
        cls.total_time = (t2 - t1) * 1000
        cls.time_per_move = 30


class TestGame7(TestGame):
    # lukaszkalisz vs Me
    @classmethod
    def setUpClass(cls):
        t1 = time.time()
        moves = '1. e4 c6 2. Nc3 d5 3. exd5 cxd5 4. Nf3 Nc6 5. Bb5 Bg4 6. O-O e6 7. d3 Nf6 8. h3 Bxf3 9. Qxf3 Bd6 \
                    10. Bg5 h6 11. Bxf6 Qxf6 12. Qxf6 gxf6 13. Bxc6 bxc6 14. a4 O-O-O 15. a5 Rhg8 16. Na4 Rg6 17. c3 Rdg8 18. g4 f5 19. f3 fxg4 20. fxg4 f5 \
                    21. Kf2 fxg4 22. hxg4 Rxg4 23. Ke2 Rg2 24. Ke1 Bg3 25. Kd1 Rg4 26. Nc5 e5 27. Rf8 Kc7 28. Rf7 Kd6 29. Nb7 Ke6 30. Rh7 Rg1 \
                    31. Kc2 Rxa1 32. Rxh6 Kf5 33. Rxc6 Bf4 34. Ra6 Rg2 35. Kb3 Bc1 36. Rxa7 Rxb2'
        cls.game = ChessGame(moves)
        t2 = time.time()
        cls.material_difference = -4
        cls.winner = 'B'
        cls.total_time = (t2 - t1) * 1000
        cls.time_per_move = 40


class TestGame8(TestGame):
    # lvpstn vs Me
    @classmethod
    def setUpClass(cls):
        t1 = time.time()
        moves = '1. e4 c6 2. f4 d5 3. e5 Bf5 4. Nf3 e6 5. d4 c5 6. Bd3 Bg6 7. O-O Nc6 8. c3 cxd4 9. cxd4 Qb6 10. Be3 Qxb2 \
                    11. Nbd2 Bxd3 12. Rb1 Qxa2 13. Rxb7 Bxf1 14. Kxf1 Rb8 15. Rc7 Qa6 16. Kg1 Bb4 17. Ng5 Nge7 18. Qh5 g6 19. Qh6 Rc8 20. Qg7 Rf8 \
                    21. Rxc8 Qxc8 22. Qxh7 Nf5 23. Nxf7 Rxf7 24. Qg8 Kd7 25. Qxf7 Kd8 26. Qf6 Kc7 27. Qg7 Kb8 28. Qxg6 Nxe3 29. Nb3 Nxd4 30. Nxd4 Qc1 \
                    31. Kf2 Qd2 32. Ne2 Bc5 33. Kf3 Nf5 34. Qxe6 Qd3 35. Kg4 Qxe2 36. Kxf5 Kb7 37. Qd7 Kb6 38. Qd8 Kb5 39. Qb8 Kc4 40. Qxa7 Bxa7 \
                    41. e6 Qxg2'
        cls.game = ChessGame(moves)
        t2 = time.time()
        cls.material_difference = -10
        cls.winner = None
        cls.total_time = (t2 - t1) * 1000
        cls.time_per_move = 40


class TestGame9(TestGame):
    # Krageven vs Me
    @classmethod
    def setUpClass(cls):
        t1 = time.time()
        moves = '1. e4 e5 2. f4 exf4 3. Nf3 Nf6 4. Nc3 Nc6 5. Bc4 Bc5 6. d4 Bb6 7. O-O O-O 8. Bxf4 d5 9. Bd3 dxe4 10. Nxe4 Re8 \
                    11. Bg5 Bxd4 12. Kh1 Bxb2 13. Rb1 Bc3 14. Nxc3 Bg4 15. Be2 Ne5 16. Nxe5 Bxe2 17. Qxe2 Qd5 18. Bxf6 gxf6 19. Qg4 Kf8 20. Nf3 Qc5 \
                    21. Nd1 Qxc2 22. Nf2 Qxf2 23. Rxf2 Re6 24. Nh4 Rae8 25. Rbf1 Re1 26. Rxf6 Rxf1 27. Rxf1 Re1 28. Rxe1 a5 29. Nf5 b6 30. Qf4 h5 \
                    31. Qxc7 b5 32. Qc8'
        cls.game = ChessGame(moves)
        t2 = time.time()
        cls.material_difference = 16
        cls.winner = 'W'
        cls.total_time = (t2 - t1) * 1000
        cls.time_per_move = 45


class TestGame10(TestGame):
    # Me vs Danijejela
    @classmethod
    def setUpClass(cls):
        t1 = time.time()
        moves = '1. e4 e5 2. f4 f6 3. fxe5 fxe5 4. Nf3 d6 5. Bc4 Qf6 6. O-O h6 7. Nc3 a6 8. Nd5 Qd8 9. d3 c6 10. Nb6 Qxb6 \
                    11. d4 c5 12. Nxe5 dxe5 13. Qh5 g6 14. Qxe5 Kd8 15. Qxh8 cxd4 16. Qxg8 d3 17. Kh1 Nd7 18. Be6 dxc2 19. Bxd7 Bxd7 20. Qxf8 Kc7 \
                    21. Qxa8 Qc6 22. Bxh6 Qxe4 23. Rac1 Bc6 24. Rfe1 Qd5 25. Re7 Kb6 26. Be3 Kb5 27. a4 Kb4 28. Rg1 b5 29. Qe8 Bxe8 30. Rxe8 Kxa4 \
                    31. Ra1 Kb3 32. Bb6 Kxb2 33. Ree1 Qc4 34. Rec1 b4 35. Bd4 Kb3 36. Rxc2 Qxc2 37. Rb1 Ka2 38. Bg1 Qxb1 39. h3 b3 40. Kh2 Qc2 \
                    41. h4 b2 42. Kh3 b1=Q 43. Bd4 Qf5 44. g4 Qbd3 45. Kh2 Qf2 46. Kh1 Qdf1'
        cls.game = ChessGame(moves)
        t2 = time.time()
        cls.material_difference = -15
        cls.winner = 'B'
        cls.total_time = (t2 - t1) * 1000
        cls.time_per_move = 30


if __name__ == '__main__':
    unittest.main(verbosity=2)