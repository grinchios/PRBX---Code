from util import fileManager, graphManager, gravityFunctions
import tsplib95

# CANVAS_HEIGHT = 1000000000
# CANVAS_WIDTH = 1000000000
CANVAS_HEIGHT = 1000
CANVAS_WIDTH = 1000
HEADLESS = False

# Load sample graph
file = fileManager.loadFile('crossover.json')
graphData = [node for node in file['vertices']]

# graphData = []
# problem = tsplib95.load('./dataset/ulysses16.tsp')
# for i in problem.get_nodes():
#     graphData.append([problem.node_coords[i][0], problem.node_coords[i][1]])

if not HEADLESS:
    # Create visualisation
    graph = graphManager.TSPGraph(CANVAS_WIDTH, CANVAS_HEIGHT, graphData)
    # graph = graphManager.TSPGraph(CANVAS_WIDTH, CANVAS_HEIGHT, graphData['vertices'])

    graph.drawCOG()
    graph.drawFurthestVertexFromCOG()

    # Tkinter start
    graph.window.mainloop()

# else:
#     for i in problem.get_nodes():
#         graphData.append(problem.node_coords[i])
    
#     myMethod = gravityFunctions.MyMethod(graphData)
#     cycle = myMethod.fullMethod()
#     print(myMethod.cycleLength(cycle))