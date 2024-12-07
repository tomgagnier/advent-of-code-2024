import unittest

import d2

matrix = d2.Matrix.from_str(
    """
    abc
    def
    ghi
    jkl
    """
)


class MyTestCase(unittest.TestCase):

    def test_get_item(self):
        self.assertEqual('j', matrix[0, 0])
        self.assertEqual('k', matrix[1, 0])
        self.assertEqual('a', matrix[0, 3])
        self.assertEqual('b', matrix[1, 3])

    def test_neighbors(self):
        self.assertEqual([(0, 1), (1, 1), (1, 0)], matrix.neighbors((0, 0)))
        self.assertEqual([(0, 2), (0, 3), (2, 3), (2, 2), (1, 2)],
                         matrix.neighbors((1, 3)))


if __name__ == '__main__':
    unittest.main()
