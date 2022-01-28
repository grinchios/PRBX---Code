# Andrew's Monotone Chain Convex Hull Algorithm
# O(n log n)

def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def monotoneChain(vertices):
    vertices.sort(key=lambda k: (k[0], k[1])) # Sort lexicographically on x then y in case of tie

    # Check for more than one vertex
    if len(vertices) <= 1:
        return vertices

    # Create lower hull
    lower = []
    for v in vertices:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], v) <=0:
            lower.pop()
        
        lower.append(v)

    # Create upper hull
    upper = []
    for v in reversed(vertices):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], v) <=0:
            upper.pop()
        
        upper.append(v)

    # Concat of lower and upper hulls gives complete convex hull
    # Last vertex omitted as it repeats at the start of the other list

    return lower[:-1] + upper[:-1]