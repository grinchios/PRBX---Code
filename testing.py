import csv
from fileinput import filename
import time
import multiprocessing as mp
import time
import os
import tsplib95
from pprint import pprint

from methods import christofides, prims
from util import gravityFunctions, createGraph

# Variables
ITERATIONS = 8
CITYCOUNT = 100
CORECOUNT = mp.cpu_count()
# CORECOUNT = 4

def getFiles():
    directory = 'dataset'
    
    # iterate over files in
    # that directory
    files = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            files.append(f)
    
    return files

def openFile(filename):
    print("\nLoading file", filename)
    problem = tsplib95.load(filename)

    graphData = []

    try:
        # print("Iterating")
        for i in problem.get_nodes():
            # print(i, end=' ')
            graphData.append([problem.node_coords[i][0], problem.node_coords[i][1]])
    
    except KeyError:
        graphData = []
    
    print("File fully loaded")
    return graphData

def main(n):
    threadNum = mp.current_process()._identity[0]
    # print('{} - Starting thread {}, {}'.format(time.time(), threadNum, n))

    # Initialise solvers
    tmpGraph = createGraph.create(n, HEIGHT=100000, WIDTH=100000)['vertices']
    CH = christofides.Christofides(tmpGraph)
    MM = gravityFunctions.MyMethod(tmpGraph)
    PR = prims.Prims(tmpGraph)

    # currentGraph = createGraph.create(n, HEIGHT=100000, WIDTH=100000)['vertices']

    # Christofides Algorithm
    CHStartTime = time.time()
    # CH.updateVertices(currentGraph)
    CHLength, _ = CH.go()
    CHTime = time.time() - CHStartTime
    # print('Christofides finished')

    # Prims algorithm
    PRStartTime = time.time()
    # PR.updateVertices(currentGraph)
    PRLength, _ = PR.go()
    PRTime = time.time() - PRStartTime
    # print('Prims finished')
    # PRLength    = 0
    # PRTime      = 0

    # My Method
    MMStartTime = time.time()
    # MM.updateVertices(currentGraph)
    MMLength, _ = MM.go()
    MMTime = time.time() - MMStartTime
    # print('Mine finished')

    csvLine = [n, CHLength, CHTime, PRLength, PRTime, MMLength, MMTime]

    return csvLine


def runTSPLIB(graphData):
    n = len(graphData)

    # Christofides Algorithm
    CHStartTime = time.time()
    print("\tInitialising Christofides")
    CH = christofides.Christofides(graphData)
    print("\tStarting Christofides")
    CHLength, _ = CH.go()
    CHTime = time.time() - CHStartTime
    print("\tFinished Christofides", str(CHTime)+"s")

    # Prims algorithm
    PRStartTime = time.time()
    # print("\tInitialising Prims")
    # PR = prims.Prims(graphData)
    # print("\tStarting Prims")
    # PRLength, _ = PR.go()
    # PRTime = time.time() - PRStartTime
    PRLength, _ = 1000000000000000000000, 0
    PRTime      = 1000000000000000000000
    print("\tFinished Prims", str(PRTime)+"s")

    # My Method
    MMStartTime = time.time()
    print("\tInitialising Gravity method")
    MM = gravityFunctions.MyMethod(graphData)
    print("\tStarting Mine")
    MMLength, _ = MM.go()
    MMTime = time.time() - MMStartTime
    print("\tFinished Mine", str(MMTime)+"s")

    csvLine = [n, CHLength, CHTime, PRLength, PRTime, MMLength, MMTime]

    return csvLine

if __name__ == '__main__':
    # print("Starting with {} cores".format(CORECOUNT))

    # # Creating CSV file helper
    # HEADER = ['city count', 'christofides', 'christofides time', 'prims', 'prims time', 'my method', 'my method time']
    # f = open('./statistics/testing-{}-{}.csv'.format(CITYCOUNT, os.getpid()), 'w+', encoding='UTF8', newline='')
    # writer = csv.writer(f)
    # writer.writerow(HEADER)

    # # Multiprocessing
    # pool = mp.Pool(CORECOUNT)

    # for cityCount in range(807, CITYCOUNT+1):
    #     print("Processing city count {}".format(cityCount))
    #     n = [cityCount for i in range(ITERATIONS)]
    #     results = pool.map(main, n)

    #     for threadResults in results:
    #         writer.writerow(threadResults)
    
    # print("Finished")

    fileList = getFiles()
    
    # TSPLIB95
    HEADER = ['filename','city count', 'christofides', 'christofides time', 'prims', 'prims time', 'my method', 'my method time']
    f = open('./statistics/TSPLIB95.csv', 'w+', encoding='UTF8', newline='')
    writer = csv.writer(f)
    writer.writerow(HEADER)

    for file in fileList:
        currentGraph = openFile(file)

        nodes = len(currentGraph)
        print("Checking file", file, nodes)

        if nodes>0 and nodes<2000:
            print("Running...")

            line = runTSPLIB(currentGraph)
            line = [file] + line
            writer.writerow(line)
    