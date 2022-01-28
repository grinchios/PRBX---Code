import math
from pprint import pprint

# Return the center of all input vertices
def getCOG(vertices):
    COG = [0,0]
    xSum, ySum = 0, 0

    # Average of all x / y coordinates, O(n)
    for vertex in vertices:
        xSum += vertex[0]
        ySum += vertex[1]

    COG[0] = xSum / len(vertices)
    COG[1] = ySum / len(vertices)

    # print("COG:", COG)
    return COG

# Iteratively find the furthest vertex from COG
def furthestVertexFromCOG(vertices, COG):
    currentFurthest = vertices[0]
    currentWorstDistance = 0
    tmpDistance = 0 # Used to prevent multiple calculations

    for vertex in vertices:
        tmpDistance = math.dist(COG, vertex)

        if  tmpDistance > currentWorstDistance:
            currentWorstDistance = tmpDistance
            currentFurthest = vertex

    return currentFurthest

# Returns in Clockwise from xMin
def boundingVertices(vertices):
    xMin, xMax, yMin, yMax = math.inf, 0, math.inf, 0
    xMinIndex, xMaxIndex, yMinIndex, yMaxIndex = -1, -1, -1, -1
        
    for i, vertex in enumerate(vertices):

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
    
    return [vertices[xMinIndex], vertices[yMaxIndex], vertices[xMaxIndex], vertices[yMinIndex]]

# Convert circuit to list of dictionaries containing edge information
def circuitToEdges(circuit):
    edges = []
    
    # Add the start vertex to the end for full circuit
    circuit.append(circuit[0])

    for i in range(len(circuit) - 1):
        A, B = circuit[i], circuit[i+1]
        edge = {
            'A': A,
            'B': B,
            'a': (A[1] - B[1]),
            'b': (B[0] - A[0]),
            'c': (A[0] * B[1] - B[0] * A[1]),
            }
    
        edges.append(edge.copy())
    return edges

def getUnvisited(vertices, circuit):
    return [v for v in vertices if v not in circuit]

# Calculate distance from linear equation to point
def edgeDistanceToVertex(edge, vertex):
    numerator = math.abs(edge['a'] * vertex[0] + edge['b'] * vertex[1] + edge['c'])
    denominator = math.sqrt(edge['a']**2 + edge['b']**2)

    print(numerator, denominator, numerator/denominator)

# Find and replace the next closest edge with two new edges
# connecting to the previous two vertices
def closestEdge(edges, vertex):
    shortestDistance = math.inf
    shortestDistanceIndex = -1
    currentDistance = -1

    for i, edge in enumerate(edges):
        currentDistance = edgeDistanceToVertex(edge, vertex)
    
    return

def fullMethod(vertices):
    circuit = []
    edges = []
    unvisited = vertices

    COG = getCOG(vertices)

    # print(boundingVertices(unvisited))
    circuit = boundingVertices(unvisited)

    # Get edge information about current circuit
    edges = circuitToEdges(circuit)
    # pprint(edges)

    unvisited = getUnvisited(vertices, circuit)

    furthestVertex = furthestVertexFromCOG(unvisited, COG)

    print(closestEdge(edges, furthestVertex))

    return circuit
