# Scott Ratchford
from tkinter import *
import random
import time
import math
import sys

# Linked List Code

class LinkedList:
    def __init__(self):
        self.next = None

    def removeNext(self):
        self.next = None
    
    def changeNext(self, next):
        self.next = next

    def insert(self, value):
        currNode = self
        while(currNode.next != None and currNode.next.value < value):
            currNode = currNode.next
        if(currNode.next == None):
            newNode = Node(value)
            currNode.next = newNode
        elif(currNode.next.value >= value):
            newNode = Node(value, currNode.next)
            currNode.next = newNode

    def __len__(self):
        return len(self.asList())

    def asList(self) -> list:
        returnList = []
        currNode = self
        if(type(currNode) != LinkedList):
            returnList.append(currNode.value)
        while(currNode.next != None):
            currNode = currNode.next
            returnList.append(currNode.value)
        return returnList

    def drawLinkedList(self, canvas: Canvas):
        canvas.delete("all")
        if(self.next == None or len(self) < 1):   # Do not draw anything if the LinkedList is empty
            return
        data = self.asList()
        currNode = self.next
        padX = 50
        padY = 50
        for index, node in enumerate(currNode.asList()):   # While there are nodes remaining
            currNode.drawNode(index, data, canvas, padX, padY, "yellow")

class Node(LinkedList):
    def __init__(self, value, next=None):
        super().__init__()
        self.value = value
        self.next = next
        self.sizeData = None
    
    def changeValue(self, value):
        self.value = value

    def drawNode(self, index, data, canvas: Canvas, padX, padY, color):
        radius = 10 + len(str(self.value)) * 1.2   # determine radius of node based on number of digits
        currX = index * ((getCanvasX(canvas) - padX) / len(data)) + padX
        currY = (getCanvasY(canvas) - padY) / 2
        canvas.create_oval(currX-radius, currY-radius, currX+radius, currY+radius, fill=color)
        canvas.create_text(currX, currY, text=str(data[index]), fill="black")

        nextIndex = index + 1
        if(nextIndex > len(data) - 1):
            return
        else:
            # draw arrows between each node
            nextX = (index + 1) * ((getCanvasX(canvas) - padX) / len(data)) + padX
            nextY = (getCanvasY(canvas) - padY) / 2
            arrowLength = (nextX - currX) * 0.5    # arrow length as a function of line length
            canvas.create_line(currX+radius, currY, nextX-radius, nextY, fill="black")
            canvas.create_line(nextX-radius-math.sqrt(arrowLength), nextY+math.sqrt(arrowLength), nextX-radius, nextY, fill="black")
            canvas.create_line(nextX-radius-math.sqrt(arrowLength), nextY-math.sqrt(arrowLength), nextX-radius, nextY, fill="black")

def animateLinkedList(data, canvas: Canvas):
    testLinkedList = LinkedList()
    for num in data:
        testLinkedList.insert(num)
        testLinkedList.drawLinkedList(canvas)


# Skip List Code

# picks the height for a node
def pickSkipNodeHeight():
    height = 1
    while (random.choice([True, False])):
        height += 1
    return height

# skip list node class
class SkipNode:
    def __init__(self, key=None, height=0):
        self.key = key
        self.next = [None] * height

# skip list class
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

    # returns an element with the given key
    def find(self, key, path=None):
        # finds path if none is given
        if path == None:
            path = self.getPath(key)
        # checks to see if the element we landed on in the path is the correct element
        if len(path) > 0:
            candidate = path[0].next[0]
            if candidate != None and candidate.key == key:
                return candidate
        # returns none if element not found
        return None

    # inserts a new node with the given key (won't insert a duplicate... yet)
    def insert(self, key):
        # creates a new node with the given key
        newNode = SkipNode(key, pickSkipNodeHeight())
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
        if nodeToRemove != None:
            for i in range(len(nodeToRemove.next)):
                path[i].next[i] = nodeToRemove.next[i]
    
    # draws SkipList on canvas
    def drawSkiplist(self, canvas: Canvas):
        pass

# Starts all data structure animations on all canvases
def startAll(data, canvas1: Canvas, canvas2: Canvas, canvas3: Canvas):
    # create Skip List
    # create RBT
    # create Fib Heap

    skipList1 = SkipList()
    linkedList2 = LinkedList()  # DEBUG
    linkedList3 = LinkedList()  # DEBUG

    for num in data:
        # dataStructure.insert(num)
        # dataStructure.drawDataStructure(canvasX)
        # root.update()
        skipList1.insert(num)
        skipList1.drawSkipList(canvas1)
        root.update()
        linkedList2.insert(num)
        linkedList2.drawLinkedList(canvas2)
        root.update()
        linkedList3.insert(num)
        linkedList3.drawLinkedList(canvas3)
        root.update()
        root.after(delaySelect.get())   # delay after every data structure is updated

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
        data.append(random.randint(minInt, maxInt))
    dataString.set(data)

root = Tk()
root.title("Data Structures Visualization Test")
root.maxsize(1920, 1080)
root.config(bg = "white")

random.seed(time.time())

# Options variables
elementsVar = IntVar(value=10)
minimumVar = IntVar(value=1)
maximumVar = IntVar(value=99)
dataString = StringVar()    # used to update dataViewLabel

# Global variables
canvasWidth = 800
canvasHeight = 400

# canvas1 label
canvas1Label = Label(root, text="Skip List", bg="white", fg="black")
canvas1Label.grid(row=0, column=0, padx=5, pady=5)
# canvas1
canvas1 = Canvas(root, width=canvasWidth, height=canvasHeight, bg="gray")
canvas1.grid(row=1, column=0, padx=10, pady=5)
# canvas2 label
canvas2Label = Label(root, text="Canvas 2", bg="white", fg="black") # DEBUG, change "Canvas 2" to correct data structure
canvas2Label.grid(row=0, column=1, padx=5, pady=5)
# canvas2
canvas2 = Canvas(root, width=canvasWidth, height=canvasHeight, bg="gray")
canvas2.grid(row=1, column=1, padx=10, pady=5)
# canvas3 label
canvas3Label = Label(root, text="Canvas 3", bg="white", fg="black") # DEBUG, change "Canvas 3" to correct data structure
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

# Data view window
dataViewLabel = Label(buttonOptionWindow, textvariable=dataString, bg="white", fg="black")
dataViewLabel.grid(row=0, column=0, padx=5, pady=5)
dataViewLabel.config(font=("Courier", 16))

# Button Window
buttonWindow = Frame(buttonOptionWindow, width=canvasWidth, height=100, bg="white")
buttonWindow.grid(row=1, column=0, padx=5, pady=5)
# Display output when button pressed
testButton = Button(buttonWindow, text="Start All", command=lambda : startAll(data, canvas1, canvas2, canvas3), bg="green", fg="white")
testButton.grid(row=0, column=0, padx=5, pady=5)
# Generate data when button pressed
randomButton = Button(buttonWindow, text="Randomize Data", command=lambda : generateData(int(elementsVar.get()), int(minimumVar.get()), int(maximumVar.get())), bg="blue", fg="white")
randomButton.grid(row=0, column=1, padx=5, pady=5)
# Reset button
sortButton = Button(buttonWindow, text="Reset All", command=clearCanvas, bg="red", fg="white")
sortButton.grid(row=0, column=2, padx=5, pady=5)
# Options Window
optionWindow = Frame(buttonOptionWindow, width=canvasWidth, height=100, bg="white")
optionWindow.grid(row=3, column=0, padx=5, pady=5)
# Wait time label
delayLabel = Label(optionWindow, text="Delay (ms)", bg="white", fg="black")
delayLabel.grid(row=0, column=2, padx=5, pady=5)
# Wait time select (lower number is faster)
delaySelect = Spinbox(optionWindow, from_=0, to=5000, increment=100)
delaySelect.grid(row=1, column=2, padx=5, pady=5)
# Number of elements label
elementsLabel = Label(optionWindow, text="Elements", bg="white", fg="black")
elementsLabel.grid(row=0, column=3, padx=5, pady=5)
# Number of elements select
elementsSelect = Spinbox(optionWindow, from_=1, to=20, increment=1, textvariable=elementsVar)
elementsSelect.grid(row=1, column=3, padx=5, pady=5)
# Minimum label
minimumLabel = Label(optionWindow, text="Minimum", bg="white", fg="black")
minimumLabel.grid(row=0, column=4, padx=5, pady=5)
# Minimum select
minimumSelect = Spinbox(optionWindow, from_=1, to=99999, increment=100, textvariable=minimumVar)
minimumSelect.grid(row=1, column=4, padx=5, pady=5)
# Maximum label
maximumLabel = Label(optionWindow, text="Maximum", bg="white", fg="black")
maximumLabel.grid(row=0, column=5, padx=5, pady=5)
# Maximum select
maximumSelect = Spinbox(optionWindow, from_=1, to=99999, increment=100, textvariable=maximumVar)
maximumSelect.grid(row=1, column=5, padx=5, pady=5)

root.mainloop()