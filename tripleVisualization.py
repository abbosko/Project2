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
from constants import *


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
            animateSkipFind(num, canvas1,skipList,root, delaySelect.get(), insertColor, True)    # draw with delays
            skipList.insert(num)
            animateSkipFind(num, canvas1, skipList,root, delaySelect.get(), insertColor, False)   # redraw with no delays
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
    animateSkipFind(num, canvas1, skipList,root, delaySelect.get(), insertColor, True)    # draw with delays
    skipList.insert(num)
    animateSkipFind(num, canvas1,skipList,root, delaySelect.get(), insertColor, False)   # redraw with no delays
    # fib heap
    fibHeap.insert(num)
    drawFibHeap(canvas2, fibHeap, nodeColor)
    # red black tree
    animateRBTFind(num, canvas3, insertColor, redBlackTree, root, delaySelect.get()) # draw before insert
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
    animateSkipFind(num, canvas1, skipList, root, delaySelect.get(),removeColor, True)    # draw with delays
    skipList.remove(num)
    root.after(delaySelect.get())
    root.update()
    animateSkipFind(num, canvas1, skipList, root, delaySelect.get(),removeColor, False)    # draw with delays
    # fib heap
    animateFibFind(canvas2, num, fibHeap, root, delaySelect.get(), removeColor)
    fibHeap.delete(num, canvas2, root, delaySelect.get(), nodeColor)
    fibHeap.findList.clear()
    drawFibHeap(canvas2, fibHeap, nodeColor)
    # red black tree
    animateRBTFind(num, canvas3, removeColor, redBlackTree, root, delaySelect.get())
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

    animateSkipFind(num, canvas1, skipList,root, delaySelect.get(), findColor, True)
    animateFibFind(canvas2, num, fibHeap,  root, delaySelect.get())
    animateRBTFind(num, canvas3, findColor, redBlackTree, root, delaySelect.get())
    # delay after every data structure is updated
    root.after(delaySelect.get())
    root.update()


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
