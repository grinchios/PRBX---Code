import json
import random
from pprint import pprint

def create(n):
    data = {}

    data['points'] = n

    height = 500
    width = 500
    data['canvas'] = {
        'height' : height,
        'width' : width
        }

    points = [[random.randint(0, width), random.randint(0, height)] for _ in range(n)]

    data['vertices'] = points

    # pprint(data)

    with open('graphs/testFile.json', 'w') as outfile:
        json.dump(data, outfile, indent = 4)
    
    return data