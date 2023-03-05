# CS 470 Team 2, February 2023
# Skip List - Sam Gaines, Scott Ratchford
# Red-Black Tree - Summer Davis, Kevin Lee
# Fibbonaci Heap - Abigail Bosko, Audrey Kim
# Animations - All teammates

from tkinter import *
import random
import time
import math
from fibheap import *
from skiplist import *
from redblacktree import *

# Calculates a radius such that the text within will fit into the circle
def calculateRadius(key):
    if(10 + (len(str(key))) * 1.2 > 12.4):
        return 10 + (len(str(key))) * 1.2   # determine radius of node based on length of the string
    else:
        return 12.4

# Skip List Code
# draw a node in skip list
def drawSkipNode(canvas: Canvas, x, y, color, node):
    radius = calculateRadius(node.key)
    canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color)
    canvas.create_text(x, y, text=str(node.key), fill="black")

# draws differently colored nodes in the path of the find operation
def animateSkipFind(key, canvas: Canvas, skipList: SkipList, color="blue", delay=True):
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
            root.after(delaySelect.get())
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

# Red Black Tree Animation
def drawRBTree(canvas: Canvas, rbt: RBTree, findList=[], outlineColor="magenta"):
    canvas.delete("all")
    allLevels = rbt.getLevels()
    # Draw the lines first
    # For each level
    for degreeIndex, level in enumerate(allLevels):
        # For each value in level
        currDegree = degreeIndex
        currY = (((getCanvasY(canvas) + (padY * 2)) / (len(allLevels) + 1)) * (currDegree + 1)) - padY
        for node in allLevels[degreeIndex]:
            levelIndex = findLevelIndex(rbt, node)
            currDegree = degreeIndex
            currX = padX + (((getCanvasX(canvas) - (padX * 2)) / (math.pow(2, currDegree) + 1)) * (levelIndex + 1))
            radius = calculateRadius(node.key)
            # Getting parent's X and Y position and drawing line to it
            if degreeIndex != 0:
                parentY = currY - ((getCanvasY(canvas) + (padY * 2)) / (len(allLevels) + 1))
                parentX = padX + (((getCanvasX(canvas) - (padX * 2)) / (math.pow(2, currDegree-1) + 1)) * (levelIndex//2 + 1))
                canvas.create_line(currX, currY, parentX, parentY, fill='black')
    # Draw the nodes second, so they are drawn over lines
    for degreeIndex, level in enumerate(allLevels):
        # For each value in level
        currDegree = degreeIndex
        currY = (((getCanvasY(canvas) + (padY * 2)) / (len(allLevels) + 1)) * (currDegree + 1)) - padY
        for node in allLevels[degreeIndex]:
            levelIndex = findLevelIndex(rbt, node)
            currDegree = degreeIndex
            currX = padX + (((getCanvasX(canvas) - (padX * 2)) / (math.pow(2, currDegree) + 1)) * (levelIndex + 1))
            radius = calculateRadius(node.key)
            color = findColor if node in findList else 'red' if node.color else 'black'
            outlineColor = outlineColor if node in findList else 'red' if node.color else 'black'
            outlineWidth = 5 if node in findList else 0
            canvas.create_oval(currX-radius, currY-radius, currX+radius, currY+radius, fill=color, outline=outlineColor, width=outlineWidth)
            canvas.create_text(currX, currY, text=node.key, fill="white")
            
def animateRBTFind(num, canvas: Canvas, findColor, rbt: RBTree):
    canvas.delete("all")
    drawRBTree(canvas, rbt)
    current = rbt.root
    allLevels = rbt.getLevels()
    currDegree = 0
    while (current != None and current != rbt.NULL):
        levelIndex = findLevelIndex(rbt, current)
        currX = padX + (((getCanvasX(canvas) - (padX * 2)) / (math.pow(2, currDegree) + 1)) * (levelIndex + 1))
        currY = (((getCanvasY(canvas) + (padY * 2)) / (len(allLevels) + 1)) * (currDegree + 1)) - padY
        radius = calculateRadius(current.key)
        outlineColor = 'red' if current.color else 'black'
        canvas.create_oval(currX-radius, currY-radius, currX+radius, currY+radius, fill=findColor, outline=outlineColor, width=5)
        canvas.create_text(currX, currY, text=current.key, fill="white")
        if current.key == num:
            break
        elif current.key > num:
            currDegree += 1
            current = current.left
        else:
            current = current.right
            currDegree += 1
        root.after(delaySelect.get())
        root.update()


# Animates the insertion of every data point into each of the three data structures
def populateAll(data, canvas1: Canvas, canvas2: Canvas, canvas3: Canvas):
    global skipList
    global fibHeap
    global redBlackTree
    
    # reset data structures
    skipList = SkipList()
    fibHeap = FibonacciHeap()
    redBlackTree = RBTree()

    # insert all elements in list
    for index, num in enumerate(data):
        # skip list
        if(index != 0):
            animateSkipFind(num, canvas1,skipList, insertColor, True)    # draw with delays
            skipList.insert(num)
            animateSkipFind(num, canvas1, skipList, insertColor, False)   # redraw with no delays
        else:
            skipList.insert(num)
        # fib heap
        fibHeap.insert(num)
        drawFibHeap(canvas2, fibHeap, insertColor)
        # red black tree
        redBlackTree.insert(num)
        drawRBTree(canvas3, redBlackTree)
        # delay after every data structure is updated
        root.after(delaySelect.get())
        root.update()

    drawSkipList(canvas1, skipList)
    drawFibHeap(canvas2, fibHeap, "yellow")
    drawRBTree(canvas3, redBlackTree)

# Animates the insertion of a specified data point into each of the three data structures
def insertIntoAll(num, canvas1: Canvas, canvas2: Canvas, canvas3: Canvas):
    global skipList
    global fibHeap
    global redBlackTree

    # do not insert duplicates
    if(skipList.find(num) != None):
        return
    # skip list
    animateSkipFind(num, canvas1, skipList, insertColor, True)    # draw with delays
    skipList.insert(num)
    animateSkipFind(num, canvas1,skipList, insertColor, False)   # redraw with no delays
    # fib heap
    fibHeap.insert(num)
    drawFibHeap(canvas2, fibHeap, nodeColor)
    # red black tree
    animateRBTFind(num, canvas3, insertColor, redBlackTree) # draw before insert
    redBlackTree.insert(num)
    drawRBTree(canvas3, redBlackTree)
    # delay after every data structure is updated
    root.after(delaySelect.get())
    root.update()

# Animates the removal of a specified data point from each of the three data structures
def removeFromAll(num, canvas1: Canvas, canvas2: Canvas, canvas3: Canvas):
    global skipList
    global fibHeap
    global redBlackTree

    # skip list
    animateSkipFind(num, canvas1, skipList, removeColor, True)    # draw with delays
    skipList.remove(num)
    root.after(delaySelect.get())
    root.update()
    animateSkipFind(num, canvas1, skipList, removeColor, False)    # draw with delays
    # fib heap
    animateFibFind(canvas2, num, fibHeap, root, delaySelect.get(), removeColor)
    fibHeap.delete(num, canvas2, root, delaySelect.get(), nodeColor)
    fibHeap.findList.clear()
    drawFibHeap(canvas2, fibHeap, nodeColor)
    # red black tree
    animateRBTFind(num, canvas3, removeColor, redBlackTree)
    redBlackTree.remove(num)
    drawRBTree(canvas3, redBlackTree)
    # delay after every data structure is updated
    root.after(delaySelect.get())
    root.update()

# Animates the search for a specified data point in each of the three data structures
def findInAll(num, canvas1: Canvas, canvas2: Canvas, canvas3: Canvas):
    global skipList
    global fibHeap
    global redBlackTree

    animateSkipFind(num, canvas1, skipList, findColor, True)
    animateFibFind(canvas2, num, fibHeap,  root, delaySelect.get())
    animateRBTFind(num, canvas3, findColor, redBlackTree)
    # delay after every data structure is updated
    root.after(delaySelect.get())
    root.update()

def getCanvasX(canvas: Canvas):
    return canvas.winfo_width()

def getCanvasY(canvas: Canvas):
    return canvas.winfo_height()

def clearCanvas():
    canvas1.delete("all")
    canvas2.delete("all")
    canvas3.delete("all")

data = []   # data values to use in the structures
def generateData(elements, minInt, maxInt):
    global data
    data = []
    for i in range(0, elements):
        tempInt = random.randint(minInt, maxInt)
        while tempInt in data:  # no duplicate values
            tempInt = random.randint(minInt, maxInt)
        data.append(tempInt)

root = Tk()
root.title("Data Structures Visualization")
root.maxsize(1920, 1080)
root.config(bg = "white")

random.seed(time.time())

# Options variables
elementsVar = IntVar(value=10)
minimumVar = IntVar(value=1)
maximumVar = IntVar(value=99)
insertVar = IntVar(value=1)
removeVar = IntVar(value=1)
findVar = IntVar(value=1)

# Color coordination variables
nodeColor = "yellow"
insertColor = "blue"
removeColor = "red"
findColor = "magenta"

# Global variables
canvasWidth = 800
canvasHeight = 400
padX = 50
padY = 50
spinboxWidth = 5
# Create all data structures
skipList = SkipList()  # create Skip List
redBlackTree = RBTree() # create RBT
fibHeap = FibonacciHeap()   # create Fib Heap

# canvas1 label
canvas1Label = Label(root, text="Skip List", bg="white", fg="black")
canvas1Label.grid(row=0, column=0, padx=5, pady=5)
# canvas1
canvas1 = Canvas(root, width=canvasWidth, height=canvasHeight, bg="gray")
canvas1.grid(row=1, column=0, padx=10, pady=5)
# canvas2 label
canvas2Label = Label(root, text="Fibonnaci Heap", bg="white", fg="black")
canvas2Label.grid(row=0, column=1, padx=5, pady=5)
# canvas2
canvas2 = Canvas(root, width=canvasWidth, height=canvasHeight, bg="gray")
canvas2.grid(row=1, column=1, padx=10, pady=5)
# canvas3 label
canvas3Label = Label(root, text="Red-Black Tree", bg="white", fg="black") # DEBUG, change "Canvas 3" to correct data structure
canvas3Label.grid(row=2, column=0, padx=5, pady=5)
# canvas3
canvas3 = Canvas(root, width=canvasWidth, height=canvasHeight, bg="gray")
canvas3.grid(row=3, column=0, padx=10, pady=5)

# Button-Option canvas label
canvasCountLabel = Label(root, text="Options", bg="white", fg="black")
canvasCountLabel.grid(row=2, column=1, padx=5, pady=5)
# Button-Option Window
buttonOptionWindow = Frame(root, width=canvasWidth, height=canvasHeight, bg="white")
buttonOptionWindow.grid(row=3, column=1, padx=5, pady=5)

# Button Window
buttonWindow = Frame(buttonOptionWindow, width=canvasWidth, height=100, bg="white")
buttonWindow.grid(row=1, column=0, padx=5, pady=5)
# Display output when button pressed
testButton = Button(buttonWindow, text="Start All", command=lambda : populateAll(data, canvas1, canvas2, canvas3), bg="green", fg="white")
testButton.grid(row=0, column=0, padx=5, pady=5)
# Generate data when button pressed
randomButton = Button(buttonWindow, text="Reset Data", command=lambda : generateData(int(elementsVar.get()), int(minimumVar.get()), int(maximumVar.get())), bg=nodeColor, fg="black")
randomButton.grid(row=0, column=1, padx=5, pady=5)
# Insert selected value
insertButton = Button(buttonWindow, text="Insert Value", command=lambda : insertIntoAll(int(insertSelect.get()), canvas1, canvas2, canvas3), bg=insertColor, fg="white")
insertButton.grid(row=0, column=2, padx=5, pady=5)
# Remove selected value
removeButton = Button(buttonWindow, text="Remove Value", command=lambda : removeFromAll(int(removeSelect.get()), canvas1, canvas2, canvas3), bg=removeColor, fg="white")
removeButton.grid(row=0, column=3, padx=5, pady=5)
# Find selected value
findButton = Button(buttonWindow, text="Find Value", command=lambda : findInAll(int(findSelect.get()), canvas1, canvas2, canvas3), bg="magenta", fg="white")
findButton.grid(row=0, column=4, padx=5, pady=5)
# Reset button
sortButton = Button(buttonWindow, text="Clear Canvas", command=clearCanvas, bg="tan4", fg="white")
sortButton.grid(row=0, column=5, padx=5, pady=5)
# Options Window
optionWindow = Frame(buttonOptionWindow, width=canvasWidth, height=100, bg="white")
optionWindow.grid(row=3, column=0, padx=5, pady=5)
# Wait time label
delayLabel = Label(optionWindow, text="Delay (ms)", bg="white", fg="black")
delayLabel.grid(row=0, column=2, padx=5, pady=5)
# Wait time select (lower number is faster)
delaySelect = Spinbox(optionWindow, from_=0, to=5000, increment=100, width=spinboxWidth)
delaySelect.grid(row=1, column=2, padx=5, pady=5)
# Number of elements label
elementsLabel = Label(optionWindow, text="Elements", bg="white", fg="black")
elementsLabel.grid(row=0, column=3, padx=5, pady=5)
# Number of elements select
elementsSelect = Spinbox(optionWindow, from_=1, to=20, increment=1, textvariable=elementsVar, width=spinboxWidth)
elementsSelect.grid(row=1, column=3, padx=5, pady=5)
# Minimum label
minimumLabel = Label(optionWindow, text="Minimum", bg="white", fg="black")
minimumLabel.grid(row=0, column=4, padx=5, pady=5)
# Minimum select
minimumSelect = Spinbox(optionWindow, from_=1, to=99999, increment=100, textvariable=minimumVar, width=spinboxWidth)
minimumSelect.grid(row=1, column=4, padx=5, pady=5)
# Maximum label
maximumLabel = Label(optionWindow, text="Maximum", bg="white", fg="black")
maximumLabel.grid(row=0, column=5, padx=5, pady=5)
# Maximum select
maximumSelect = Spinbox(optionWindow, from_=1, to=99999, increment=100, textvariable=maximumVar, width=spinboxWidth)
maximumSelect.grid(row=1, column=5, padx=5, pady=5)
# Insert label
insertLabel = Label(optionWindow, text="Insert", bg=insertColor, fg="white")
insertLabel.grid(row=0, column=6, padx=5, pady=5)
# Insert select
insertSelect = Spinbox(optionWindow, from_=minimumVar.get(), to=maximumVar.get(), increment=1, textvariable=insertVar, width=spinboxWidth)
insertSelect.grid(row=1, column=6, padx=5, pady=5)
# Remove label
removeLabel = Label(optionWindow, text="Remove", bg=removeColor, fg="white")
removeLabel.grid(row=0, column=7, padx=5, pady=5)
# Remove select
removeSelect = Spinbox(optionWindow, from_=minimumVar.get(), to=maximumVar.get(), increment=1, textvariable=removeVar, width=spinboxWidth)
removeSelect.grid(row=1, column=7, padx=5, pady=5)
# Find label
findLabel = Label(optionWindow, text="Find", bg="magenta", fg="white")
findLabel.grid(row=0, column=8, padx=5, pady=5)
# Remove select
findSelect = Spinbox(optionWindow, from_=minimumVar.get(), to=maximumVar.get(), increment=1, textvariable=findVar, width=spinboxWidth)
findSelect.grid(row=1, column=8, padx=5, pady=5)

root.mainloop()
