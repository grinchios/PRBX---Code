import math
from pprint import pprint

class MyMethod():
    def __init__(self, vertices):
        self.vertices = vertices
        self.circuit = []
        self.edges = []
        self.unvisited = vertices
        self.COG = [0,0]

        # Get initial circuit
        self.circuit = self.boundingVertices()

        # Get edge information about current circuit
        self.edges = self.circuitToEdges()

        # Initial unvisited vertices
        self.unvisited = self.getUnvisited()

    # Return the center of all input vertices
    def getCOG(self, vertices):
        xSum, ySum = 0, 0

        # Average of all x / y coordinates, O(n)
        for vertex in vertices:
            xSum += vertex[0]
            ySum += vertex[1]

        self.COG[0] = xSum / len(vertices)
        self.COG[1] = ySum / len(vertices)

        # print("COG:", COG)
        return self.COG

    # Iteratively find the furthest vertex from COG
    def furthestVertexFromCOG(self, Debug=False):
        currentFurthest = self.unvisited[0]
        currentWorstDistance = 0
        tmpDistance = 0 # Used to prevent multiple calculations

        for vertex in self.unvisited:
            tmpDistance = math.dist(self.COG, vertex)
            if Debug: print(vertex, tmpDistance)

            if  tmpDistance > currentWorstDistance:
                currentWorstDistance = tmpDistance
                currentFurthest = vertex
        if Debug: print()
        return currentFurthest

    # Returns in Clockwise from xMin
    def boundingVertices(self):
        xMin, xMax, yMin, yMax = math.inf, 0, math.inf, 0
        xMinIndex, xMaxIndex, yMinIndex, yMaxIndex = -1, -1, -1, -1
            
        for i, vertex in enumerate(self.unvisited):

            if vertex[0] < xMin:
                xMin = vertex[0]
                xMinIndex = i
            
            elif vertex[0] > xMax:
                xMax = vertex[0]
                xMaxIndex = i

            if vertex[1] < yMin:
                yMin = vertex[1]
                yMinIndex = i
            
            elif vertex[1] > yMax:
                yMax = vertex[1]
                yMaxIndex = i    

        # Remove duplicates if exactly 2 or 3 vertices
        corners = [] 
        for corner in [
            self.unvisited[xMinIndex], self.unvisited[yMaxIndex], 
            self.unvisited[xMaxIndex], self.unvisited[yMinIndex]]:

            if corner not in corners:
                corners.append(corner)

        return corners

    def gradiant(self, A, B):
        return (B[1] - A[1]) / (B[0] - A[0])

    def edgeCreation(self, A, B):
        edge = {
            'A': A,
            'B': B,
            'a': (A[1] - B[1]),
            'b': (B[0] - A[0]),
            'c': (A[0] * B[1] - B[0] * A[1]),
            'len': self.edgeLength(A, B),
            'm': self.gradiant(A, B)
            }
        
        return edge

    # Convert circuit to list of dictionaries containing edge information
    def circuitToEdges(self):
        edges = []
        
        # Add the start vertex to the end for full circuit
        self.circuit.append(self.circuit[0])

        for i in range(len(self.circuit) - 1):
            A, B = self.circuit[i], self.circuit[i+1]
            edge = self.edgeCreation(A, B)
        
            edges.append(edge.copy())
        return edges

    def getUnvisited(self):
        return [v for v in self.vertices if v not in self.circuit]

    # Calculate distance from linear equation to point
    def edgeDistanceToVertex(self, edge, vertex):
        A, B, m = edge['A'], edge['B'], edge['m']
        c = A[1] - m * A[0]
        
        mInverse = -1 / m
        x = (c - vertex[1] + mInverse * vertex[0]) / (-m + mInverse)

        C = [x, m * x + c]

        AC, BC, AB = self.edgeLength(A, C), self.edgeLength(B, C), edge['len']
        AV, BV = self.edgeLength(A, vertex), self.edgeLength(B, vertex)

        print(A, B, vertex, C, 'm', m, 'c', c, 'x', x, 'AC', AC, 'BC', BC, 'AB', AB, 'AV', AV, 'BV', BV)

        # Closest point is within segment AB
        if AC + BC == AB:
            return self.edgeLength(C, vertex) 
        
        # Point is closest to A
        elif AV < BV:
            return AV
        
        # Point is closest to B
        else:
            return BV

    def replaceEdgeWithEdges(self, edges, edgeIndex, vertex):
        # Edge from old A to new vertex
        A1, B1 = edges[edgeIndex]['A'], vertex
        edge1 = self.edgeCreation(A1, B1)

        # Edge from new vertex to old B
        A2, B2 = vertex, edges[edgeIndex]['B']
        edge2 = self.edgeCreation(A2, B2)

        # Replace old edge with new edges
        newEdges = edges[0:edgeIndex] + [edge1, edge2] + edges[edgeIndex+1:]

        return newEdges

    # Calculate distance from A to B
    def edgeLength(self, A, B):
        return math.sqrt((B[0] - A[0])**2 + (B[1] - A[1])**2)

    # Find and replace the next closest edge with two new edges
    # connecting to the previous two vertices
    def closestEdge(self, edges, vertex, Debug=False):
        shortestDistance = math.inf
        shortestDistanceIndex = -1
        currentDistance = -1

        if Debug: print(self.vertices)
        for i, edge in enumerate(edges):
            currentDistance = self.edgeDistanceToVertex(edge, vertex)
            currentDistanceCOG = self.edgeDistanceToVertex(edge, self.COG)

            if Debug: print(
                'A:', self.vertices.index(edge['A']), 'B:', self.vertices.index(edge['B']), 'Shortest:', shortestDistance,
                'Current:', currentDistance, edge['len'] / currentDistance,
                edge['len'] / currentDistanceCOG,
                abs(edge['len'] / currentDistanceCOG - edge['len'] / currentDistance))

            if currentDistance < shortestDistance:
                shortestDistanceIndex = i
                shortestDistance = currentDistance

        if Debug: print('\nBest\n', 'A:', self.vertices.index(edges[shortestDistanceIndex]['A']), 
                'B:', self.vertices.index(edges[shortestDistanceIndex]['B']), 
                '\nShortest:', shortestDistance)
        
        return self.replaceEdgeWithEdges(edges, shortestDistanceIndex, vertex)

    def convertEdgesToVertices(self, edges):
        circuit = []
        for edge in edges:
            circuit.append(edge['A'])
        
        # Add final B to form complete cycle
        circuit.append(edge['B'])

        return circuit

    def step(self):
        if len(self.unvisited) == 0:
            return
        
        self.getCOG(self.unvisited)
        print('COG', self.COG, 'From:', len(self.unvisited))

        # Find next best vertex and remove from unvisited
        furthestVertex = self.furthestVertexFromCOG(Debug=False)
        print('Furthest Vertex', furthestVertex)
        print('Unvisited', len(self.unvisited), self.unvisited)
        self.unvisited.remove(furthestVertex)
    
        print()

        self.edges = self.closestEdge(self.edges, furthestVertex, Debug=True)
        return self.convertEdgesToVertices(self.edges)

    def fullMethod(self):
        # print(boundingVertices(unvisited))
        self.circuit = self.boundingVertices()

        # Get edge information about current circuit
        self.edges = self.circuitToEdges()

        # Initial unvisited vertices
        self.unvisited = self.getUnvisited()

        i = 0
        while len(self.unvisited) != 0:
            COG = self.getCOG(self.unvisited)

            # Find next best vertex and remove from unvisited
            furthestVertex = self.furthestVertexFromCOG()
            self.unvisited.remove(furthestVertex)

            print('Iteration:', i, 'exploring', furthestVertex)

            self.edges = self.closestEdge(self.edges, furthestVertex)
            i += 1

        return self.convertEdgesToVertices(self.edges)
