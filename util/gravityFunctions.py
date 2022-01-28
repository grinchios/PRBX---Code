import math

def getCOG(vertices):
    COG = [0,0]
    xSum, ySum = 0, 0

    # Average of all x / y coordinates, O(n)
    for vertex in vertices:
        xSum += vertex[0]
        ySum += vertex[1]

    COG[0] = xSum / len(vertices)
    COG[1] = ySum / len(vertices)

    print("COG:", COG)
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