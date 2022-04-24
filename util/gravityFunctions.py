import math
from pprint import pprint

from numpy import short
from util import convexHull

class MyMethod():
    def __init__(self, vertices):
        self.vertices = vertices
        self.circuit = []
        self.edges = []
        self.unvisited = vertices
        self.totalCOGDistance = [0 for vertex in self.unvisited]
        self.COG = [0,0]

        # Get initial circuit
        self.boundingConvexHull()

        # Get edge information about current circuit
        self.edges = self.circuitToEdges()

        # Initial unvisited vertices
        self.unvisited = self.getUnvisited()

    def updateVertices(self, vertices):
        self.vertices = vertices
        self.unvisited = vertices
        self.totalCOGDistance = [0 for vertex in self.unvisited]
        self.COG = [0,0]

        # Get initial circuit
        self.boundingConvexHull()

        # Get edge information about current circuit
        self.edges = self.circuitToEdges()

        # Initial unvisited vertices
        self.unvisited = self.getUnvisited()

    def boundingConvexHull(self):
        self.circuit = convexHull.monotoneChain(self.unvisited)
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
        currentFurthest = [self.unvisited[0]]
        currentWorstIndex = 0
        tmpDistance = 0 # Used to prevent multiple calculations
        if Debug: print('Vertex to COG Distances:', self.totalCOGDistance)

        for vertex in self.unvisited:
            currentVertexIndex = self.vertices.index(vertex)
            tmpDistance = math.dist(self.COG, vertex)
            if Debug: print('Vertex->COG distance', self.vertices.index(vertex), vertex, tmpDistance)

            self.totalCOGDistance[currentVertexIndex] += tmpDistance

            if self.totalCOGDistance[currentVertexIndex] == self.totalCOGDistance[currentWorstIndex]:
                currentFurthest.append(vertex)

            if self.totalCOGDistance[currentVertexIndex] > self.totalCOGDistance[currentWorstIndex]:
                currentWorstIndex = currentVertexIndex

                if len(currentFurthest) > 1:
                    currentFurthest = [vertex]

                else:
                    currentFurthest[0] = vertex
            
        if Debug: print()
        return currentFurthest

    def gradiant(self, A, B):
        demoninator = B[0] - A[0]
        if demoninator == 0:
            return 0
        return (B[1] - A[1]) / (demoninator)

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
    def edgeDistanceToVertex(self, edge, vertex, Debug=False):
        A, B, m = edge['A'], edge['B'], edge['m']
        c = A[1] - m * A[0]
        
        if m==0:
            mInverse = 0
            x = 0
        else:
            mInverse = -1 / m
            x = (c - vertex[1] + mInverse * vertex[0]) / (-m + mInverse)

        C = [x, m * x + c]

        AC, BC, AB = self.edgeLength(A, C), self.edgeLength(B, C), edge['len']
        AV, BV = self.edgeLength(A, vertex), self.edgeLength(B, vertex)

        if A[0] != B[0]:
            onLine = 0 <= (C[0] - A[0]) / (B[0] - A[0]) <= 1
        elif A[1] != B[1]:
            onLine = 0 <= (C[1] - A[1]) / (B[1] - A[1]) <= 1
        else:
            onLine = True

        if Debug and onLine: print(
            A, B, vertex, C, '\nm', m, 'c', c, 'x', x, '\nAC', AC, 'BC', BC, 'AB', AB, 'AC+BC', AC + BC)

        # Closest point is within segment AB
        if onLine:
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
        bestDistance = math.inf
        bestDistanceIndex = -1
        currentDistance = -1

        for i, edge in enumerate(edges):
            currentDistance = self.edgeDistanceToVertex(edge, vertex, Debug=Debug)
            currentDistanceCOG = self.edgeDistanceToVertex(edge, self.COG)

            if Debug: print(
                'A:', self.vertices.index(edge['A']), 'B:', self.vertices.index(edge['B']), 'Shortest:', bestDistance,
                'Current:', currentDistance, 'Len/AB-C:', edge['len'] / currentDistance,
                'Len/AB-COG:', edge['len'] / currentDistanceCOG,
                abs(edge['len'] / currentDistanceCOG - edge['len'] / currentDistance),
                abs(currentDistance*(edge['len'] / currentDistanceCOG) - currentDistanceCOG*(edge['len'] / currentDistance)))
            
            # currentDistance = abs(edge['len'] / currentDistanceCOG - edge['len'] / currentDistance)
            # currentDistance = edge['len'] / currentDistance

            if Debug: print()

            if currentDistance == bestDistance and self.unvisited:
                # Select edge that is closer to future COG
                if len(self.unvisited) > 1:
                    self.unvisited.remove(vertex)
                    self.getCOG(self.unvisited)
                    self.unvisited.append(vertex)
                else:
                    self.getCOG(self.unvisited)
                
                if currentDistanceCOG < self.edgeDistanceToVertex(edges[bestDistanceIndex], self.COG):
                    bestDistanceIndex = i
                    bestDistance = currentDistance

            elif currentDistance < bestDistance:
                bestDistanceIndex = i
                bestDistance = currentDistance

        if Debug: print('\nBest\n', 'A:', self.vertices.index(edges[bestDistanceIndex]['A']), 
                'B:', self.vertices.index(edges[bestDistanceIndex]['B']), 
                '\nShortest:', bestDistance)
        
        return self.replaceEdgeWithEdges(edges, bestDistanceIndex, vertex)

    def convertEdgesToVertices(self, edges):
        circuit = []
        pprint(edges)
        for edge in edges:
            print(edge)
            circuit.append(edge['A'])
        
        # Add final B to form complete cycle
        circuit.append(edge['B'])

        return circuit

    def cycleLength(self, cycle):
        length = 0
        for edge in cycle:
            length += edge['len']
        
        return length

    def step(self, Debug=False):
        if len(self.unvisited) == 0:
            return
        
        self.getCOG(self.unvisited)
        if Debug: print('COG', self.COG, 'From:', len(self.unvisited))

        # Find next best vertex and remove from unvisited
        furthestVertex = self.furthestVertexFromCOG(Debug=False)

        for vertex in furthestVertex:
            print('Furthest Vertex', vertex, self.vertices.index(vertex))
            
        if Debug: print('Unvisited', len(self.unvisited), self.unvisited)
    
        if Debug: print()

        if len(furthestVertex) > 1:
            shortestLength = math.inf
            bestEdges = []

            for vertex in furthestVertex:
                tmpEdges = self.closestEdge(self.edges, vertex, Debug=False)

                currentLength = self.cycleLength(tmpEdges)

                if currentLength < shortestLength:
                    bestVertex = vertex
                    shortestLength = currentLength
                    bestEdges = tmpEdges
                
                if Debug: print('Current shortest cycle: ', shortestLength, self.vertices.index(bestVertex), currentLength)

            self.unvisited.remove(bestVertex)
            self.edges = bestEdges

        else:
            self.edges = self.closestEdge(self.edges, furthestVertex[0], Debug=True)
            self.unvisited.remove(furthestVertex[0])

        return self.convertEdgesToVertices(self.edges)

    def go(self, Debug=False):
        i = 0
        while len(self.unvisited) != 0:
            self.getCOG(self.unvisited)

            # Find next best vertex and remove from unvisited
            furthestVertex = self.furthestVertexFromCOG(Debug=False)
                
            if len(furthestVertex) > 1:
                shortestLength = math.inf
                bestEdges = []

                for vertex in furthestVertex:
                    tmpEdges = self.closestEdge(self.edges, vertex, Debug=False)

                    currentLength = self.cycleLength(tmpEdges)

                    if currentLength < shortestLength:
                        bestVertex = vertex
                        shortestLength = currentLength
                        bestEdges = tmpEdges
                    
                self.unvisited.remove(bestVertex)
                self.edges = bestEdges

            else:
                self.edges = self.closestEdge(self.edges, furthestVertex[0], Debug=False)
                self.unvisited.remove(furthestVertex[0])

            i += 1

        length = self.cycleLength(self.edges)
        # print('My Method: ', length)

        return length, self.edges
