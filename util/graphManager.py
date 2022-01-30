from textwrap import wrap
from tkinter import *
import math
from tkinter.tix import COLUMN
from turtle import color

from matplotlib.pyplot import text
from util import gravityFunctions, convexHull, createGraph
from methods import bruteforce

class TSPGraph():
    def __init__(self, width, height, vertices):
        self.windowWidth = width
        self.windowHeight = height

        # Variables
        self.initVariables(vertices)

        # Setup Methods
        self.window = self.create(self.windowWidth, self.windowHeight)        

        self.drawVertices()

    def initVariables(self, vertices):
        # Variables
        self.frames = {}
        self.BBState = False
        self.BBLines = []
        self.CHState = False
        self.CHLines = []
        self.BFState = False
        self.BFLines = []
        self.BFPath = []
        self.COG = []
        self.COGID = 0
        self.furthestVertex = []
        self.furthestVertexID = 0

        self.myMethodPath = []
        self.myMethodLines = []
        self.myMethodState = False

        # Inputs
        self.vertices = vertices
        self.unvisited = vertices

        # Method
        self.myMethod = gravityFunctions.MyMethod(vertices)

    # Create whole GUI and attach inputs to relevant functions
    def create(self, width, height):
        master = Tk()
        master.title("TSP Gravity - Callum Pritchard")
        master.resizable(True, False) # Y axis not resizeable

        # Graph canvas
        w = Canvas(master,
                width=width,
                height=height,
                background='white')
        w.grid(row=0, column=0, sticky=W,  padx=(0, 50), rowspan=10)

        # Right side of window, options
        self.frames['vertexCOG'] = Button(master, text = 'vertex -> COG', width=12, command=self.drawFurthestVertexFromCOG)
        self.frames['vertexCOG'].grid(row=0, column=1, padx=(0, 10))

        self.frames['edgeCOG'] = Button(master, text="Draw COG", width=12, command=self.drawCOG)
        self.frames['edgeCOG'].grid(row=0, column=2, padx=(0, 50))

        self.frames['boundingBox'] = Button(master, text = 'Toggle BB', width=12, command=self.bbToggle)
        self.frames['boundingBox'].grid(row=1, column=1, padx=(0, 10))

        self.frames['convexHull'] = Button(master, text="Toggle CH", width=12, command=self.chToggle)
        self.frames['convexHull'].grid(row=1, column=2, padx=(0, 50))

        self.frames['bruteforce'] = Button(master, text = 'Bruteforce', width=12, command=self.bruteforceToggle)
        self.frames['bruteforce'].grid(row=2, column=1, padx=(0, 10))

        self.frames['mymethod'] = Button(master, text = 'My Method', width=12, command=self.myMethodToggle)
        self.frames['mymethod'].grid(row=2, column=2, padx=(0, 50))

        self.frames['newGraph'] = Button(master, text = 'New Graph', width=12, command=self.newGraph)
        self.frames['newGraph'].grid(row=3, column=1, padx=(0, 10))

        self.frames['nextStep'] = Button(master, text = 'Next Step', width=12, command=self.myMethodIterate)
        self.frames['nextStep'].grid(row=4, column=1, padx=(0, 10))

        self.n = StringVar(value=10)
        self.frames['newGraphVertices'] = Spinbox(master, from_=3, to=20, textvariable=self.n, wrap=False)
        self.frames['newGraphVertices'].grid(row=3, column=2, padx=(0, 10))

        return w

    def newGraph(self):
        newGraph = createGraph.create(n=int(self.n.get()))

        self.initVariables(newGraph['vertices'])
        self.window.delete('all')

        self.drawVertices()

    def myMethodIterate(self):
        # Update unvisited
        self.unvisited = self.myMethod.unvisited

        for asset in self.myMethodLines:
            self.window.delete(asset)

        if len(self.myMethodPath) > 0:
            self.highlightVertices(self.myMethodPath)
            self.myMethodLines = self.drawEdges(self.myMethodPath)

        if len(self.unvisited) == 0:
            print('Finished Graphing')
            return

        self.myMethodPath = self.myMethod.step()

        if len(self.unvisited) != 0: 
            self.drawCOG()
            self.drawFurthestVertexFromCOG()

    def myMethodToggle(self):
        self.myMethodState = not self.myMethodState
        
        if self.myMethodState and self.myMethodPath == []:
            # self.myMethodPath = convexHull.monotoneChain(self.vertices)
            self.myMethodPath = self.myMethod.fullMethod()

            # Update unvisited
            self.unvisited = self.myMethod.unvisited

            self.highlightVertices(self.myMethodPath)
            self.myMethodLines = self.drawEdges(self.myMethodPath)
        
        elif self.myMethodState and self.myMethodPath != []:
            self.myMethodLines = self.drawEdges(self.myMethodPath)

        else:
            for asset in self.myMethodLines:
                self.window.delete(asset)

    def highlightVertices(self, vertices):
        for vertex in vertices:
            self.createCircle(vertex, colour='orange')

    def drawEdges(self, circuit, colour='black', dash=None):
        edges = []

        for i in range(len(circuit)-1):
            edges.append(self.window.create_line(circuit[i][0], circuit[i][1], circuit[i+1][0], circuit[i+1][1], fill=colour, dash=dash))
        
        edges.append(self.window.create_line(circuit[0][0], circuit[0][1], circuit[len(circuit)-1][0], circuit[len(circuit)-1][1], fill=colour, dash=dash))

        return edges

    # Show Bruteforce Path
    def bruteforceToggle(self):
        self.BFState = not self.BFState
        
        if self.BFState and self.BFPath == []:
            bf = bruteforce.Bruteforce(self.vertices)
            self.BFPath = bf.go()
            self.BFLines = self.drawEdges(self.BFPath, colour='red')

        elif self.BFState and self.BFPath != []:
            self.BFLines = self.drawEdges(self.BFPath, colour='red')
        
        else:
            for asset in self.BFLines:
                self.window.delete(asset)

            self.BFLines = []

    # Use Andrews Monotone Chain Algorithm
    def chToggle(self):
        self.CHState = not self.CHState

        if self.CHState and self.CHLines == []:
            CH = convexHull.monotoneChain(self.vertices)
            self.CHLines = self.drawEdges(CH, colour='orange', dash=(5,1))

        else:
            for asset in self.CHLines:
                self.window.delete(asset)

            self.CHLines = []

    # Get smallest / largest x and y values
    def bbToggle(self):
        self.BBState = not self.BBState

        if self.BBState:
            xMin, xMax, yMin, yMax = math.inf, 0, math.inf, 0
        
            for vertex in self.vertices:
                if vertex[0] < xMin:
                    xMin = vertex[0]
                
                elif vertex[0] > xMax:
                    xMax = vertex[0]

                if vertex[1] < yMin:
                    yMin = vertex[1]
                
                elif vertex[1] > yMax:
                    yMax = vertex[1]
            
            self.BBLines.append(self.window.create_line(xMin, 0, xMin, self.windowHeight, dash=(4,2)))
            self.BBLines.append(self.window.create_line(xMax, 0, xMax, self.windowHeight, dash=(4,2)))
            self.BBLines.append(self.window.create_line(0, yMin, self.windowWidth, yMin, dash=(4,2)))
            self.BBLines.append(self.window.create_line(0, yMax, self.windowWidth, yMax, dash=(4,2)))
        
        else:
            for asset in self.BBLines:
                self.window.delete(asset)

            self.BBLines = []

    # Draw vertices given as input
    def drawVertices(self):
        print(self.vertices)
        for i, vertex in enumerate(self.vertices):
            self.createCircle(vertex, label=i)

    def createCircle(self, vertex, r = 5, colour=None, label=None): #center coordinates, radius
        x = vertex[0]
        y = vertex[1]

        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r

        # Draw text slightly above circle
        if label != None:
            self.window.create_text(x, y+r*2, text=label)

        return self.window.create_oval(x0, y0, x1, y1, fill=colour)
    
    # Draw COG and remove old one if present
    def drawCOG(self):
        if self.COGID != 0:
            self.window.delete(self.COGID)
        
        self.COGID = self.createCircle(self.myMethod.COG, colour='red')

    # Draw furthest vertex from COG
    def drawFurthestVertexFromCOG(self):
        if self.furthestVertexID != 0:
            self.window.delete(self.furthestVertexID)
        
        self.furthestVertex = self.myMethod.furthestVertexFromCOG()
        self.furthestVertexID = self.createCircle(self.furthestVertex, colour='blue')
        