import os
from PIL import Image, ImageFont, ImageDraw
from ai.astar.node import Node
from ai.astar.board import *
# Board dimensions
BOARD_HEIGHT = 0
BOARD_WIDTH = 0

NeighborMap = {}

# Read board config from txt file and returns a list with all nodes
def readFromTxt(filename):
    global BOARD_HEIGHT     
    global BOARD_WIDTH

    nodeGraph = []
    numWords = 0
    numLines = 0

    with open(filename, 'r') as file:
        for x, line in enumerate(file):
            numLines += 1
            for y, char in enumerate(line):
                if char is not '\n':
                    numWords += 1
                    insertNode(x, y, char, nodeGraph)

    BOARD_HEIGHT = numLines                
    BOARD_WIDTH = numWords // numLines
    return nodeGraph


# Add node to node list
def insertNode(x, y, char, nodeGraph):
    nodeGraph.append(Node(x, y, char))


# Creates neighbors list for a node
def createNeighbors(node, nodeGraph):
    #If you want diagonals put in dirs : [-1,-1], [1,1], [1, -1], [-1,1]]
    dirs = [[1,0], [0,1], [-1, 0], [0,-1]]
            
    #for dir in dirs:
    #    n = node.x + dir[0], node.y + dir[1]
    #    if n in NeighborMap:
    #        print("Find neighbor")
    #        print(node.neighbors)
    #        node.addNeighbor(NeighborMap[n])
    #    else:
    #        for newNode in nodeGraph:
    #            if(newNode.x == node.x + dir[0] and newNode.y == node.y + dir[1]):
    #                NeighborMap[n] = newNode
    #                node.addNeighbor(newNode)
    pos = (node.x, node.y)
    if pos in NeighborMap:
        
        node.neighbors = NeighborMap[pos]
    else:
        for dir in dirs:
            for newNode in nodeGraph:
                    if(newNode.x == node.x + dir[0] and newNode.y == node.y + dir[1]):
                        node.addNeighbor(newNode)
        NeighborMap[pos] = node.neighbors

# Get board color based on content
def getColor(content):
    # Water
    if content is 'w':
        return '#0000ff' # Blue

    # Mountains 
    if content is 'm':
        return '#808080' # Gray

    # Forests
    if content is 'f':
        return '#004d00' # Dark green

    # Grassland
    if content is 'g':
        return '#00e600' # Light green

    # Roads
    if content is 'r':
        return '#c68c53' # Light brown

    # Start
    if content is 'A':
        return '#ffffff' # Black

    # Goal
    if content is 'B':
        return '#ffff00' # Yellow

    # Blocked node
    if content is '#':
        return 'gray'

    # Default
    return 'white'

# Draw board with path, border and closed nodes.
def drawBoard(path, border, closed, nodeGraph, filename):
    im = Image.new('RGB', (BOARD_WIDTH*100,BOARD_HEIGHT*100), (255,255,255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 25)
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            node = list(filter(lambda n: n.x == i and n.y == j, nodeGraph))[0]
            dr.rectangle([(0+j*100,0+i*100), (100+j*100,100+i*100)], fill=getColor(node.cellContent), outline = "black")

            # White circle indicates that this node was in border list
            if node in border and node not in path:
                dr.ellipse((0+j*100+30, 0+i*100+30, 100+j*100-30, 100+i*100-30), fill='black')

            # Red circle indicates that this node was in closed list
            elif node in closed and node not in path:
                dr.ellipse((0+j*100+30, 0+i*100+30, 100+j*100-30, 100+i*100-30), fill='red')

            # Draw text for start node
            if node.cellContent is 'A':
                dr.text((0+j*100+10,0+i*100+10), "START", (0,0,0), font=font)

            # Draw text for goal node
            if node.cellContent is 'B':
                dr.text((0+j*100+10,0+i*100+10), "GOAL", (0,0,0), font=font)
    

    # Line from start to goal
    dr.line([(n.y*100 + 50, n.x*100 + 50) for n in path], fill="pink", width=15)

    # Save image
    im.save("img/{0}.png".format(filename), "PNG")   
    
