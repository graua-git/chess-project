import unittest
from Chess.Coord import *

class CoordTestCase(unittest.TestCase):
    def test_1(self):
        x, y = 0, 0
        expected = 'a1'
        result = Coord(x, y)
        self.assertEqual(result, expected, msg='{} != {}'.format(result, expected))
    
    def test_2(self):
        x, y = 7, 0
        expected = 'h1'
        result = Coord(x, y)
        self.assertEqual(result, expected, msg='{} != {}'.format(result, expected))
    
    def test_3(self):
        x, y = 0, 7
        expected = 'a8'
        result = Coord(x, y)
        self.assertEqual(result, expected, msg='{} != {}'.format(result, expected))
    
    def test_4(self):
        x, y = 7, 7
        expected = 'h8'
        result = Coord(x, y)
        self.assertEqual(result, expected, msg='{} != {}'.format(result, expected))

    def test_5(self):
        x, y = 3, 4
        expected = 'd5'
        result = Coord(x, y)
        self.assertEqual(result, expected, msg='{} != {}'.format(result, expected))
    
    def test_error_1(self):
        x, y = 0, 8
        expected = 'Error'
        try:
            result = Coord(x, y)
        except InvalidCoordError:
            return
        self.assertEqual(result, expected, msg='{} != {}'.format(result, expected))

    def test_error_2(self):
        x, y = 8, 0
        expected = 'Error'
        try:
            result = Coord(x, y)
        except InvalidCoordError:
            return
        self.assertEqual(result, expected, msg='{} != {}'.format(result, expected))

    def test_error_3(self):
        x, y = -1, 5
        expected = 'Error'
        try:
            result = Coord(x, y)
        except InvalidCoordError:
            return
        self.assertEqual(result, expected, msg='{} != {}'.format(result, expected))

    def test_error_4(self):
        x, y = 3, -1
        expected = 'Error'
        try:
            result = Coord(x, y)
        except InvalidCoordError:
            return
        self.assertEqual(result, expected, msg='{} != {}'.format(result, expected))

        
if __name__ == '__main__':
    unittest.main(verbosity=2)