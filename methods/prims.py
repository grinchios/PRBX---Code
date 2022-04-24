import math

class Prims():
    def __init__(self, vertices):
        self.vertices = vertices
        self.dists = self.generateDistance()

    def updateVertices(self, vertices):
        self.vertices = vertices
        self.dists = self.generateDistance()
    
    def generateDistance(self):
        n = len(self.vertices)

        dists = [[0] * n for i in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                dists[i][j] = dists[j][i] = math.dist(self.vertices[i], self.vertices[j])

        return dists
    
    def indexToPath(self, indexes):
        path = []
        for index in indexes:
            path.append(self.vertices[index])
        
        return path

    def pathLength(self, path):
        pathLength = 0

        for i in range(len(path) - 1):
            pathLength += math.dist(path[i], path[i+1])
        
        return pathLength

    def go(self):
        V = len(self.vertices)
        selected = [0 for i in range(V)]
        path = []
        noEdge = 0
        
        selected[0] = True

        while (noEdge < V - 1):
            # For every vertex in the set S, find the all adjacent vertices
            #, calculate the distance from the vertex selected at step 1.
            # if the vertex is already in the set S, discard it otherwise
            # choose another vertex nearest to selected vertex  at step 1.
            minimum = math.inf
            x = 0
            y = 0
            for i in range(V):
                if selected[i]:
                    for j in range(V):
                        if ((not selected[j]) and self.dists[i][j]):
                            # not in selected and there is an edge
                            if minimum > self.dists[i][j]:
                                minimum = self.dists[i][j]
                                x = i
                                y = j

            selected[y] = True
            path.append(y)
            noEdge += 1

        path[:] = path[:] + [path[0]]

        cycle = self.indexToPath(path)

        return self.pathLength(cycle), cycle

