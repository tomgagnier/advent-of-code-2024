import unittest

import d2
from utilities.d2 import Coordinate

matrix = d2.StringMatrix.from_multiline_str(
    """
    abc
    def
    ghi
    jkl
    """
)


class TestD2(unittest.TestCase):

    def test_coordinate(self):
        self.assertEqual(2, Coordinate((2, 1)).i)
        self.assertEqual(2, Coordinate((2, 1))[0])
        self.assertEqual(1, Coordinate((2, 1)).j)
        self.assertEqual(1, Coordinate((2, 1))[1])
        self.assertEqual(Coordinate((5, 6)), Coordinate((2, 1)) + Coordinate((3, 5)))
        self.assertEqual(Coordinate((-1, -4)), Coordinate((2, 1)) - Coordinate((3, 5)))
        self.assertEqual('(1, 8)', str(Coordinate((1, 8))))
        self.assertEqual([Coordinate((2, 3)), Coordinate((5, 4))],
                         list(Coordinate((1, -2)).translate(
                             [Coordinate((1, 5)), Coordinate((4, 6))])))

    def test_max(self):
        self.assertEqual(3, matrix.max_i)
        self.assertEqual(4, matrix.max_j)

    def test_get_item(self):
        self.assertEqual('j', matrix[0, 0])
        self.assertEqual('k', matrix[1, 0])
        self.assertEqual('a', matrix[0, 3])
        self.assertEqual('b', matrix[1, 3])

    def test_set_item(self):
        matrix[0, 1] = '1'
        self.assertEqual('1', matrix[0, 1])

    def test_repr(self):
        self.assertEqual('abc\ndef\nghi\njkl', str(matrix))

    def test_get(self):
        self.assertEqual('h', matrix.get((1, 1)))
        self.assertEqual('', matrix.get((5, 5), ''))
        self.assertIsNone(matrix.get((5, 5)))

    def test_iter(self):
        self.assertEqual(
            [d2.Coordinate(t) for t in
             [(0, 0), (1, 0), (2, 0),
              (0, 1), (1, 1), (2, 1),
              (0, 2), (1, 2), (2, 2),
              (0, 3), (1, 3), (2, 3)]],
            list(matrix))

    def test_find(self):
        self.assertIsNone(matrix.find(lambda x: x == 'z'))
        coordinate = Coordinate((1, 2))
        find = matrix.find(lambda x: x == 'e')
        self.assertEqual(coordinate, find)
        self.assertEqual(Coordinate((0, 0)), matrix.find(lambda x: x == 'j'))

    def test_neighbors(self):
        self.assertEqual(Coordinate.from_tuples((0, 1), (1, 1), (1, 0)),
                         list(matrix.neighbors(Coordinate((0, 0)))))
        self.assertEqual(Coordinate.from_tuples((0, 2), (0, 3), (2, 3), (2, 2), (1, 2)),
                         list(matrix.neighbors(Coordinate((1, 3)))))


if __name__ == '__main__':
    unittest.main()
