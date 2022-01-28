import json

def loadFile(filename):
    with open('graphs/' + filename, 'r') as f:
        data = json.load(f)
    
    return data