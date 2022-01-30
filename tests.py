import unittest

# Modules to Test
from util import gravityFunctions

class TestGravityFunctions(unittest.TestCase):
    def setUp(self):
        PLACEHOLDER = True

    def testEdgeDistanceToVertex(self):
        self.gravity = gravityFunctions.MyMethod([[2, 1], [5, 7]])
        A = [2, 1]
        B = [5, 7]
        AB = self.gravity.edgeLength(A, B)
        edges = [
            {'A': A, 'B': B, 'a': -6, 'b': 3, 'c': 9, 'len': AB, 'm': self.gravity.gradiant(A, B)},
            {'A': B, 'B': A, 'a': 6, 'b': -3, 'c': -9, 'len': AB, 'm': self.gravity.gradiant(B, A)}
            ]
        
        distance = self.gravity.edgeDistanceToVertex(edges[0], [8, 5])

        self.assertAlmostEqual(distance, 3.605551, places=2)

if __name__ == '__main__':
    unittest.main()