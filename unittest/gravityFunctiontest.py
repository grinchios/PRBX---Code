import unittest

# Modules to Test
from util import gravityFunctions

class TestGravityFunctions(unittest.TestCase):
    def setUp(self):
        PLACEHOLDER = True
    
    def circuitToEdgesTest(self):
        circuit = gravityFunctions.circuitToEdges([[2, 1], [5, 7]])
        self.assertEqual(circuit, [])