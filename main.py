from util import fileManager, graphManager, gravityFunctions

CANVAS_HEIGHT = 500
CANVAS_WIDTH = 500

# Load sample graph
graphData = fileManager.loadFile('testFile.json')

# Create visualisation
graph = graphManager.TSPGraph(CANVAS_WIDTH, CANVAS_HEIGHT, graphData['vertices'])

# Calculate and draw bounding box
# graph.bbToggle()
# graph.chToggle()
# graph.myMethodToggle()
graph.drawCOG()
graph.drawFurthestVertexFromCOG()

# graph.bruteforceToggle()

# Tkinter start
graph.window.mainloop()