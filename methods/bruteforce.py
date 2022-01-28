import itertools
import math

class Bruteforce():
    def __init__(self, vertices):
        self.vertices = vertices
        self.current_best_path = []
        self.current_best_distance = 100000000000000000
        self.current_best_edges = []

    def go(self):
        for path in itertools.permutations(self.vertices):
            path = path + (path[0],)
            distance = 0

            for i in range(1, len(path)):
                V1 = path[i-1]
                V2 = path[i]
                distance += math.dist(V1, V2)
            
            if distance < self.current_best_distance:
                self.current_best_path = path
                self.current_best_distance = distance

        return self.current_best_path[:-1]