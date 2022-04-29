from textwrap import wrap
from tkinter import *
import math
from tkinter.tix import COLUMN
from turtle import color

from matplotlib.pyplot import text
from util import gravityFunctions, convexHull, createGraph
from methods import bruteforce, christofides, heldkarp

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
        self.CHState = False
        self.CHLines = []
        self.BFState = False
        self.BFLines = []
        self.BFPath = []

        self.ChristofidesState = False
        self.ChristofidesLines = []
        self.ChristofidesPath = []

        self.KarpState = False
        self.KarpLines = []
        self.KarpPath = []


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
        # self.frames['vertexCOG'] = Button(master, text = 'removed feature', width=12, command=self.drawFurthestVertexFromCOG)
        # self.frames['vertexCOG'].grid(row=0, column=1, padx=(0, 10))

        self.frames['edgeCOG'] = Button(master, text="Draw COG", width=12, command=self.drawCOG)
        self.frames['edgeCOG'].grid(row=0, column=2, padx=(0, 50))

        self.frames['christofides'] = Button(master, text = 'Christofides', width=12, command=self.christofidesToggle)
        self.frames['christofides'].grid(row=1, column=1, padx=(0, 10))

        self.frames['convexHull'] = Button(master, text="Toggle CH", width=12, command=self.chToggle)
        self.frames['convexHull'].grid(row=1, column=2, padx=(0, 50))

        self.frames['bruteforce'] = Button(master, text = 'Bruteforce', width=12, command=self.bruteforceToggle)
        self.frames['bruteforce'].grid(row=2, column=1, padx=(0, 10))

        self.frames['mymethod'] = Button(master, text = 'My Method', width=12, command=self.myMethodToggle)
        self.frames['mymethod'].grid(row=2, column=2, padx=(0, 50))

        self.frames['heldkarp'] = Button(master, text = 'Held-Karp', width=12, command=self.heldKarpToggle)
        self.frames['heldkarp'].grid(row=3, column=1, padx=(0, 10))

        self.frames['newGraph'] = Button(master, text = 'New Graph', width=12, command=self.newGraph)
        self.frames['newGraph'].grid(row=4, column=1, padx=(0, 10))

        self.n = StringVar(value=10)
        self.frames['newGraphVertices'] = Spinbox(master, from_=3, to=20, textvariable=self.n, wrap=False)
        self.frames['newGraphVertices'].grid(row=4, column=2, padx=(0, 10))

        self.frames['nextStep'] = Button(master, text = 'Next Step', width=12, command=self.myMethodIterate)
        self.frames['nextStep'].grid(row=5, column=1, padx=(0, 10))

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
            print('Finished Graphing: ', self.myMethod.cycleLength(self.myMethod.edges))
            return

        self.myMethodPath = self.myMethod.step()

        if len(self.unvisited) != 0: 
            self.drawCOG()
            self.drawFurthestVertexFromCOG()

    def heldKarpToggle(self):
        self.KarpState = not self.KarpState
        
        if self.KarpState and self.KarpPath == []:
            hk = heldkarp.HeldKarp(self.vertices)
            _, self.KarpPath = hk.go()
            self.KarpLines = self.drawEdges(self.KarpPath, colour='blue')

        elif self.KarpState and self.KarpPath != []:
            self.KarpLines = self.drawEdges(self.KarpPath, colour='blue')
        
        else:
            for asset in self.KarpLines:
                self.window.delete(asset)

            self.KarpLines = []

    def myMethodToggle(self):
        self.myMethodState = not self.myMethodState
        
        if self.myMethodState and self.myMethodPath == []:
            # self.myMethodPath = convexHull.monotoneChain(self.vertices)
            # self.myMethodPath = self.myMethod.go()
            # self.myMethodPath = self.myMethod.convertEdgesToVertices(self.myMethodPath)

            # Update unvisited
            self.unvisited = self.myMethod.unvisited

            while self.unvisited:
                self.myMethodPath = self.myMethod.step()
                self.unvisited = self.myMethod.unvisited

            self.highlightVertices(self.myMethodPath)
            self.myMethodLines = self.drawEdges(self.myMethodPath)
            print('Finished Graphing: ', self.myMethod.cycleLength(self.myMethod.edges))
        
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

    # Show Christofides Path
    def christofidesToggle(self):
        self.ChristofidesState = not self.ChristofidesState
        
        if self.ChristofidesState and self.ChristofidesPath == []:
            ch = christofides.Christofides(self.vertices)
            _, self.ChristofidesPath = ch.go()
            self.ChristofidesLines = self.drawEdges(self.ChristofidesPath, colour='blue')

        elif self.ChristofidesState and self.ChristofidesPath != []:
            self.ChristofidesLines = self.drawEdges(self.ChristofidesPath, colour='blue')
        
        else:
            for asset in self.ChristofidesLines:
                self.window.delete(asset)

            self.ChristofidesLines = []

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

        for vertex in self.furthestVertex:
            self.furthestVertexID = self.createCircle(vertex, colour='blue')
        