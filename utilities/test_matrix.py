import unittest

from matrix import Matrix

matrix = Matrix.from_str("""abc
def
ghi
jkl""")


class MyTestCase(unittest.TestCase):

    def test_neighbors(self):
        self.assertEqual('j', matrix[0, 0])
        self.assertEqual({(0,1), (1, 0), (1,1)}, matrix.neighbors(0, 0))

    def test_to_str(self):
        self.assertEqual('jg', matrix.to_str([(0,0), (0,1)]))


if __name__ == '__main__':
    unittest.main()
