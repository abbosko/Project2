import random
from tkinter import *
from constants import *

def pickHeight():
    height = 1
    while (random.choice([True, False])):
        height += 1
    return height
class SkipNode:
    def __init__(self, key=None, height=0):
        self.key = key
        self.next = [None] * height
    
    def __str__(self) -> str:
        return "[" + str(self.key) + "]"

    def __eq__(self, __o: object) -> bool:
        if(type(__o) != SkipNode):  # cannot be equal to another type of object
            return False
        return self.key == __o.key
class SkipList:
    def __init__(self):
        self.head = SkipNode()
 
    # gets an array of the last node on each level whose key is less than the given key
    # helper function
    def getPath(self, key):
        # initializes array to hold the nodes where we "shift down" a level
        path = [None] * len(self.head.next)
        # searches down the list for the key, but stops when it hits the bottom
        ptr = self.head
        for i in range(len(self.head.next)-1, -1, -1):
            while ptr.next[i] != None and ptr.next[i].key < key:
                ptr = ptr.next[i]
            path[i] = ptr
        # return the path taken down the list
        return path

    # gets an array of the last node on each level whose key is less than the given key
    # helper function
    def getPath(self, key):
        # initializes array to hold the nodes where we "shift down" a level
        path = [None] * len(self.head.next)
        # searches down the list for the key, but stops when it hits the bottom
        ptr = self.head
        for i in range(len(self.head.next)-1, -1, -1):
            while ptr.next[i] != None and ptr.next[i].key < key:
                ptr = ptr.next[i]
            path[i] = ptr
        # return the path taken down the list
        return path

    # returns an element with the given key
    def find(self, key, path=None):
        # finds path if none is given
        if(path == None):
            path = self.getPath(key)
        # checks to see if the element we landed on in the path is the correct element
        if(len(path) > 0):
            candidate = path[0].next[0]
            if(candidate != None and candidate.key == key):
                return candidate
        # returns none if element not found
        return None 

    # inserts a new node with the given key
    def insert(self, key):
        # creates a new node with the given key
        newNode = SkipNode(key, pickHeight())
        # adds another level of pointer to the head, if necessary
        while len(self.head.next) < len(newNode.next):
            self.head.next.append(None)
        # inserts node and updates pointers in each height level the node reaches
        path = self.getPath(key)
        for i in range(len(newNode.next)):
            newNode.next[i] = path[i].next[i]
            path[i].next[i] = newNode

    # removes a node with the given key
    def remove(self, key):
        # updates pointers around each height level the node is in
        path = self.getPath(key)
        nodeToRemove = self.find(key, path)
        if(nodeToRemove == None):
            return
        for i in range(len(nodeToRemove.next)):
            path[i].next[i] = nodeToRemove.next[i]
        while(None in self.head.next):
            self.head.next.remove(None)

    # returns list of nodes in row r
    def getRow(self, r):
        # iterate through given row r
        nodes = []
        nodePtr = self.head
        while nodePtr.next[r] != None:
            nodePtr = nodePtr.next[r]
            nodes.append(nodePtr)
        return nodes

    # return list of lists of nodes in each row
    def getRows(self):
        # return None if there are no nodes
        if(len(self.head.next) == 0):
            return None
        # call getRow for each row in skip list and add to rows list.
        rows = []
        for i in range(len(self.head.next)):
            rows.append(self.getRow(i))
        return rows

    def getFullPath(self, key):
        # initializes array to hold the nodes where we "shift down" a level
        rows = self.getRows()
        fullPath = []
        # searches down the list for the key, but stops when it hits the bottom
        ptr = self.head
        for i in range(len(self.head.next)-1, -1, -1):
            while ptr.next[i] != None and ptr.next[i].key < key:
                # -1 indicates Head
                if ptr.key == None:
                    column = -1
                else:
                    column = rows[i].index(ptr)
                fullPath.append((i, column))
                ptr = ptr.next[i]
            # -1 indicates Head
            if ptr.key == None:
                column = -1
            else:
                column = rows[i].index(ptr)
            fullPath.append((i, column))
        # add final element
        if ptr.next[0] and ptr.next[0].key == key:
            fullPath.append((0, rows[0].index(ptr.next[0])))
        # return the FULL path taken down the list
        # tuple of (row, column)
        return fullPath

# Skip List Animation
# draw a node in skip list
def drawSkipNode(canvas: Canvas, x, y, color, node):
    radius = calculateRadius(node.key)
    canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color)
    canvas.create_text(x, y, text=str(node.key), fill="black")

# draws differently colored nodes in the path of the find operation
def animateSkipFind(key, canvas: Canvas, skipList: SkipList, root, dT, color="blue", delay=True):
    canvas.delete("all")
    drawSkipList(canvas, skipList)
    global padX
    global padY
    path = skipList.getFullPath(key)
    allRows = skipList.getRows()
    # inner functions to determine the X and Y values of the given node
    def findX(node):
        index = allRows[0].index(node)
        return (((getCanvasX(canvas) - 2 * padX) / (len(allRows[0]) + 2)) * (index + 2)) + padX
    def findY(allRows, rowIndex):
        return (((getCanvasY(canvas) - 2 * padY) / (len(allRows) + 1)) * (rowIndex + 1)) + padY
    for element in path:
        currX = findX(allRows[element[0]][element[1]])
        if(element[1] == -1):   # head node
            leftX = ((getCanvasX(canvas) - 2 * padX) / (len(allRows[0]) + 2)) + padX
            currY = (((getCanvasY(canvas) - 2 * padY) / (len(allRows) + 1)) * (len(allRows) - element[0])) + padY
            radius = 10 + (len(str("H")) + 1) * 1.2   # determine radius of node based on length of the string "H"
            canvas.create_oval(leftX-radius, currY-radius, leftX+radius, currY+radius, fill=color)
            canvas.create_text(leftX, currY, text="H", fill="white")
        else:                   # not head node
            if((len(allRows) - element[0] - 1) < 0):
                currY = findY(allRows, len(allRows) - element[0])
            else:
                currY = findY(allRows, len(allRows) - element[0] - 1)
            radius = calculateRadius(allRows[element[0]][element[1]].key)
            canvas.create_oval(currX-radius, currY-radius, currX+radius, currY+radius, fill=color)
            canvas.create_text(currX, currY, text=str(allRows[element[0]][element[1]].key), fill="white")
        if(delay):  # delay between highlights
            root.after(dT)
            root.update()

def drawSkipList(canvas: Canvas, skipList: SkipList):
    canvas.delete("all")
    global padX
    global padY
    allRows = skipList.getRows()
    topY = (((getCanvasY(canvas) - 2 * padY) / (len(allRows) + 1))) + padY
    bottomY = (((getCanvasY(canvas) - 2 * padY) / (len(allRows) + 1)) * len(allRows)) + padY
    # create tuples of (key, x) to determine the x position on upper rows
    bottomRow = []
    leftX = (((getCanvasX(canvas) - 2 * padX) / (len(allRows[0]) + 2))) + padX
    canvas.create_line(leftX, bottomY, leftX, topY, fill="black") # draw vertical lines between nodes
    for rowIndex, node in enumerate(allRows[0]):    # determine x values for the bottom row
        currX = (((getCanvasX(canvas) - 2 * padX) / (len(allRows[0]) + 2)) * (rowIndex + 2)) + padX # Reference this one for an example
        bottomRow.append((node.key, currX)) # tuple of (key, x)
        canvas.create_line(currX, bottomY, currX, topY, fill="black") # draw vertical lines between nodes

    leftX = (((getCanvasX(canvas) - 2 * padX) / (len(allRows[0]) + 2))) + padX
    rightX = (((getCanvasX(canvas) - 2 * padX) / (len(allRows[0]) + 2)) * (len(allRows[0]) + 1)) + padX
    for colIndex, col in enumerate(allRows):
        currY = (((getCanvasY(canvas) - 2 * padY) / (len(allRows) + 1)) * (colIndex + 1)) + padY
        canvas.create_line(leftX, currY, rightX, currY, fill="black") # draw horizontal lines between nodes
        # draw head nodes
        radius = 10 + (len(str("H")) + 1) * 1.2   # determine radius of node based on length of the string "H"
        canvas.create_oval(leftX-radius, currY-radius, leftX+radius, currY+radius, fill="orange")
        canvas.create_text(leftX, currY, text="H", fill="black")

    # create blank 2D list of tuples of (SkipNode, x, y)
    nodeMatrix = [[None]*len(bottomRow) for i in range(len(allRows))]
    for index, row in enumerate(reversed(allRows)):
        currY = (((getCanvasY(canvas) - 2 * padY) / (len(allRows) + 1)) * (index + 1)) + padY
        for rowIndex, node in enumerate(row):
            found = True
            for bottomIndex, element in enumerate(bottomRow):
                if(element[0] == node.key):
                    drawSkipNode(canvas, element[1], currY, nodeColor,node)
                    nodeMatrix[index][bottomIndex] = (node, currX, currY)
                    found = True
            if(not found):  # found is a bool, so duplicates do not yet appear
                currX = (((getCanvasX(canvas) - 2 * padX) / (len(allRows[0]) + 2)) * (rowIndex + 2)) + padX  # for now, currX is determined per row
                drawSkipNode(canvas, currX, currY, nodeColor, node)
                nodeMatrix[rowIndex][bottomIndex] = (node, currX, currY)
