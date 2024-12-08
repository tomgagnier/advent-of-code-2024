import unittest

import d2

matrix = d2.Matrix.from_multiline_str(
    """
    abc
    def
    ghi
    jkl
    """
)


class MyTestCase(unittest.TestCase):

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
        self.assertEqual([
            (0, 0), (1, 0), (2, 0),
            (0, 1), (1, 1), (2, 1),
            (0, 2), (1, 2), (2, 2),
            (0, 3), (1, 3), (2, 3),
        ], list(matrix))

    def test_find(self):
        self.assertEqual((0, 0), matrix.find(lambda x: x == 'j'))
        self.assertEqual((1, 2), matrix.find(lambda x: x == 'e'))
        self.assertIsNone(matrix.find(lambda x: x == 'z'))

    def test_neighbors(self):
        self.assertEqual([(0, 1), (1, 1), (1, 0)], matrix.neighbors((0, 0)))
        self.assertEqual([(0, 2), (0, 3), (2, 3), (2, 2), (1, 2)],
                         matrix.neighbors((1, 3)))


if __name__ == '__main__':
    unittest.main()
