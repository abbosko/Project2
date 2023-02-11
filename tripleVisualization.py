# CS 470 Team 2, February 2023
# Skip List - Sam Gaines and Scott Ratchford
# Red-Black Tree -
# Fibbonaci Heap - 
# Animations - Scott Ratchford

from tkinter import *
import random
import time
import math
import sys

# Linked List Code

class LinkedList:
    def __init__(self):
        self.next = None

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

    # non-functional, dummy
    def remove(self, value) -> bool:
        return False

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
        global padX
        global padY
        canvas.delete("all")
        if(self.next == None or len(self) < 1):   # Do not draw anything if the LinkedList is empty
            return
        thisData = self.asList()
        currNode = self.next
        for index, node in enumerate(currNode.asList()):   # While there are nodes remaining
            currNode.drawNode(index, thisData, canvas, padX, padY, "yellow")

class Node(LinkedList):
    def __init__(self, value, next=None):
        super().__init__()
        self.value = value
        self.next = next
        self.sizeData = None
    
    def changeValue(self, value):
        self.value = value

    def drawNode(self, index, data, canvas: Canvas, padX, padY, color):
        radius = calculateRadius(self.value)
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

# Skip List Code

# picks the height for a node
def pickHeight():
    height = 1
    while (random.choice([True, False])):
        height += 1
    return height

# skip list node class
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

    def drawSkipNode(self, canvas: Canvas, x, y, color):
        radius = calculateRadius(self.key)
        canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color)
        canvas.create_text(x, y, text=str(self.key), fill="black")

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

    # draws differently colored nodes in the path of the find operation
    def animateFind(self, key, canvas: Canvas, delay=True):
        canvas.delete("all")
        self.drawSkipList(canvas)
        global padX
        global padY
        path = self.getFullPath(key)
        allRows = self.getRows()
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
                canvas.create_oval(leftX-radius, currY-radius, leftX+radius, currY+radius, fill="blue")
                canvas.create_text(leftX, currY, text="H", fill="black")
            else:                   # not head node
                if((len(allRows) - element[0] - 1) < 0):
                    currY = findY(allRows, len(allRows) - element[0])
                else:
                    currY = findY(allRows, len(allRows) - element[0] - 1)
                radius = calculateRadius(allRows[element[0]][element[1]].key)
                canvas.create_oval(currX-radius, currY-radius, currX+radius, currY+radius, fill="blue")
                canvas.create_text(currX, currY, text=str(allRows[element[0]][element[1]].key), fill="black")
            if(delay):  # delay between highlights
                root.after(delaySelect.get())
                root.update()

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
        if(nodeToRemove != None):
            for i in range(len(nodeToRemove.next)):
                path[i].next[i] = nodeToRemove.next[i]

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
    
    def drawSkipList(self, canvas: Canvas):
        canvas.delete("all")
        global padX
        global padY
        allRows = self.getRows()
        maxLen = 0
        for index, row in enumerate(allRows):
            if(len(row) > maxLen):
                maxLen = len(row)
        topY = (((getCanvasY(canvas) - 2 * padY) / (len(allRows) + 1))) + padY
        bottomY = (((getCanvasY(canvas) - 2 * padY) / (len(allRows) + 1)) * len(allRows)) + padY
        # create tuples of (key, x) to determine the x position on upper rows
        bottomRow = []
        leftX = (((getCanvasX(canvas) - 2 * padX) / (len(allRows[0]) + 2)) * (1)) + padX
        canvas.create_line(leftX, bottomY, leftX, topY, fill="black") # draw vertical lines between nodes
        for rowIndex, node in enumerate(allRows[0]):    # determine x values for the bottom row
            currX = (((getCanvasX(canvas) - 2 * padX) / (len(allRows[0]) + 2)) * (rowIndex + 2)) + padX # currX = (((getCanvasX(canvas) - 2 * padX) / (len(allRows[0]) + 1)) * (rowIndex + 1)) + padX
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
                color = "yellow"
                found = True
                for bottomIndex, element in enumerate(bottomRow):
                    if(element[0] == node.key):
                        node.drawSkipNode(canvas, element[1], currY, color)
                        nodeMatrix[index][bottomIndex] = (node, currX, currY)
                        found = True
                if(not found):  # found is a bool, so duplicates do not yet appear
                    currX = (((getCanvasX(canvas) - 2 * padX) / (len(allRows[0]) + 2)) * (rowIndex + 2)) + padX  # for now, currX is determined per row
                    node.drawSkipNode(canvas, currX, currY, color)
                    nodeMatrix[rowIndex][bottomIndex] = (node, currX, currY)

# Fib Heap code
class FibNode:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = self.left = self.right = self.child = None
        self.color = 'N'     # for find
        self.mark = False    # flag for find 
        self.k = 'N'
    def drawFibNode(self, canvas: Canvas, X, Y, color):
        radius = 10 + len(str(self.key)) * 1.2   # determine radius of node based on number of digits
        # currX = index * ((canvas.winfo_width() - padX) / len(rootList)) + padX
        # currY = (canvas.winfo_height()- padY) / 2
        canvas.create_oval(X-radius, Y-radius, X+radius, Y+radius, fill=color)
        canvas.create_text(X, Y, text=str(self.key), fill="black")
        

class FibonacciHeap:
    def __init__(self):
        self.min = None
        self.nodeCount = 0
        self.finder = None
    
    def addToRootList(self, node):
        if self.min is None:
            self.min = node
        else:
            node.right = self.min.right
            node.left = self.min
            self.min.right.left = node
            self.min.right = node
    
    def removeFromRootList(self, node):
        if node == self.min:
            self.min = node.right
        node.left.right = node.right
        node.right.left = node.left

    # when consolidating, this adds the smaller tree to the bigger tree
    def addToTree(self, bigger, smaller):
        self.removeFromRootList(bigger)
        if(smaller.right == smaller):
            self.min = smaller
        bigger.left = bigger
        bigger.right = bigger
        bigger.parent = smaller
        if(smaller.child == None):
            smaller.child = bigger
        bigger.right = smaller.child 
        bigger.left = smaller.child.left
        smaller.child.left.right = bigger
        smaller.child.left = bigger
        if bigger.key < smaller.child.key:
            smaller.child = bigger
        smaller.degree += 1
        smaller.mark = False

    def addToChildList(self, parent, node):
        if parent.child is None:
            parent.child = node
        else:
            node.left = parent.child
            node.right = parent.child.right
            parent.child.right.left = node
            parent.child.right = node
    
    def removeFromChildList(self, parent, node):
        # if only one child 
        if(parent.child == parent.child.right):
            parent.child = None
        # when found node cut it out by reset ptrs
        elif parent.child == node:
            parent.child = node.right
            node.right.parent = parent
        # cut out
        node.left.right = node.right
        node.right.left = node.left

    def insert(self, key):
        # make new node, set pointers to itself for doubly linked
        newNode = FibNode(key)
        newNode.left = newNode
        newNode.right = newNode
        # add it to root list
        self.addToRootList(newNode)
        # set as new min if smallest or no min
        if self.min is None or newNode.key < self.min.key:
                self.min = newNode
        self.nodeCount += 1

    def find_min(self):
        return self.min.key

    # This iterates through the doubly linked list starting at min, helps with consolidate
    def iterate(self, head):
        node = end = head
        stop = False
        while True:
            if node == end and stop is True:  # means it is back at the starting point
                break
            elif node == end:
                stop = True
            yield node
            node = node.right

    def extract_min(self):
        if(self.min == None):
            # print("Heap empty, can't extract")
            return
        else:
            oldMin = self.min
            if(oldMin.child != None):   # if the min has children
                # for every child of old minimum add to root list
                children = [x for x in self.iterate(oldMin.child)]
                for i in children:
                    self.addToRootList(i)
                    if(i.key < self.min.key):
                        self.min = i
                    i.parent = None
            self.removeFromRootList(oldMin)
            self.min = oldMin.right
            if(oldMin == oldMin.right):
                self.min = None
            else: 
                self.min = oldMin.right
                self.consolidate()
            self.nodeCount -= 1

    def consolidate(self):
        aux = [None] * int(math.log(self.nodeCount) * 2)
        #get root list
        array = [node for node in self.iterate(self.min)]
        while array != []:
            first = array[0]
            degree = first.degree
            array.remove(first)
            while aux[degree] is not None:
                # if already have tree of that degree
                second = aux[degree]
                # grab that value 
                if first.key > second.key: # this is to ensure that the second is larger than the first
                    temp = first
                    first = second
                    second = temp
                self.addToTree(second, first) # link tree
                aux[degree] = None #reset to 0
                degree += 1    
            aux[degree] = first
        self.min = None
        # Find min node
        for i in aux:
            if i is not None:
                if self.min is None or i.key < self.min.key:
                    self.min = i
    
    def cut(self, node, parent):
        # no longer a child so remove from child list 
        self.removeFromChildList(parent, node)
        parent.degree -= 1
        self.addToRootList(node)
        node.parent = None
        node.mark = False
    
    def cascadeCut(self, node):
        ptr = node.parent
        if(ptr != None):
            if(node.mark == False):
                node.mark = True
            else:
                self.cut(node, ptr)
                self.cascadeCut(ptr)

    # decrease key used for delete
    def decrease_key(self, node, val):
        # not decreasing
        if val > node.key:
            return None
        # set new key value to node
        node.key = val
        parent = node.parent
        # if node is now smaeller than its parent, cut and refactor
        if parent != None and node.key < parent.key:
            self.cut(node, parent)
            self.cascadeCut(parent)
        # if node is now smallest, set as min
        if node.key < self.min.key:
            self.min = node

    def find(self, start,  val):
        ptr = start
        ptr.color = 'Y'
        if(ptr.key == val):
            ptr.color = 'N'
            self.finder = ptr
            return 
        else:
            if(ptr.child != None):
                self.find(start.child, val)
            if(ptr.right.color != 'Y'):
                self.find(start.right, val)
        ptr.color = 'N'

    def delete(self, val):
        if(self.min == None):
            print("Error: Heap Empty")
        elif(self.min.key == val):
            self.extract_min()
        else:
            self.finder = None
            self.find(self.min, val)
            node = self.finder
            if(node == None):
                print("not found")
            else:
                # Decreasing the value of the node to new min
                self.decrease_key(node, self.min.key - 1)
                # Calling Extract_min function to delete node
                self.extract_min()
 
    def display(self):
        ptr1 = self.min
        if(ptr1 == None):
            print("The Heap is Empty")
        else:
            print("The root nodes of Heap are: ")
            print(ptr1.key, "->", end='')
            ptr = ptr1.right
            while(ptr != ptr1):
                print(ptr.key,"->", end='')
                ptr = ptr.right
            print()
            print("Node count", self.nodeCount)
    
    def drawFibHeap(self, canvas): 
        # self.populateRootList()
        # canvas.delete("all")
        # if(self.rootList == None or len(self.rootList) < 1):   # Do not draw anything if the LinkedList is empty
        node = self.min
        node.drawFibNode(canvas, 50, 50,  'yellow')
        if(node.child != None):
            self.drawFib(node.child, canvas, 70,70, node)
        elif (node.right):
            self.drawFib(node.right, canvas, 70,70, node)
        else: 
            return

    def drawFib(self, node, canvas,  x, y, begin):

        ptr = node
        ptr.k = 'Y'
        color = 'yellow'

        if(ptr == begin):
            ptr.k = 'N'
            return 

        else:
            if( ptr == self.min): color = 'cyan'
            ptr.drawFibNode(canvas, x, y,  color)
            if(ptr.child != None):
                y+=20
                self.drawFib(node.child,canvas, x, y, begin)
            if (ptr.right.k != 'Y'):
                x+=20
                self.drawFib(node.right, canvas, x, y,  begin);
        ptr.k = 'N'
       

# Calculates a radius such that the text within will fit into the circle
def calculateRadius(key):
    return 10 + (len(str(key))) * 1.2   # determine radius of node based on length of the string

# Animates the insertion of every data point into each of the three data structures
def populateAll(data, canvas1: Canvas, canvas2: Canvas, canvas3: Canvas):
    global skipList
    global fibHeap
    # global rbt
    
    # reset data structures
    skipList = SkipList()
    fibHeap = FibonacciHeap()

    for index, num in enumerate(data):
        if(index != 0):
            skipList.animateFind(num, canvas1, True)    # draw with delays
            skipList.insert(num)
            fibHeap.insert(num)
            skipList.animateFind(num, canvas1, False)   # redraw with no delays
        else:
            skipList.insert(num)
            fibHeap.insert(num)
        root.after(delaySelect.get())   # delay after every data structure is updated
        root.update()
    skipList.drawSkipList(canvas1)
    fibHeap.drawFibHeap(canvas2)
    # fibHeap
    # rbt

# Animates the insertion of a specified data point into each of the three data structures
def insertIntoAll(num, canvas1: Canvas, canvas2: Canvas, canvas3: Canvas):
    global skipList
    global fibHeap
    # global rbt

    # do not insert duplicates
    if(skipList.find(num) != None):
        return
    # check in fib heap
    # check in rbt

    skipList.animateFind(num, canvas1, True)    # draw with delays
    skipList.insert(num)
    skipList.animateFind(num, canvas1, False)   # redraw with no delays
    root.after(delaySelect.get())
    root.update()

    # fibHeap

    fibHeap.insert(num)
    fibHeap.drawFibHeap(canvas2)
    # rbt

    root.after(delaySelect.get())   # delay after every data structure is updated

# Animates the removal of a specified data point from each of the three data structures
def removeFromAll(num, canvas1: Canvas, canvas2: Canvas, canvas3: Canvas):
    global skipList
    global fibHeap
    # global rbt

    # do not insert duplicates
    if(skipList.find(num) != None):
        return
    # check in fib heap
    # check in rbt
 
    skipList.animateFind(num, canvas1, True)    # draw with delays
    skipList.insert(num)
    fibHeap.delete(num)
    fibHeap.drawFibHeap(canvas2)
    root.update()
    skipList.animateFind(num, canvas1, False)   # redraw with no delays
    root.after(delaySelect.get())
    root.update()

    root.after(delaySelect.get())   # delay after every data structure is updated

# Animates the search for a specified data point in each of the three data structures
def findInAll(num, canvas1: Canvas, canvas2: Canvas, canvas3: Canvas):
    global skipList
    global fibHeap
    # global redBlackTree

    # dataStructure.animateFind(num)
    # root.update()

    skipList.animateFind(num, canvas1)
    root.update()

    # fibHeap.animateFind(num, canvas2)
    # root.update()
    
    # RBT

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
        tempInt = random.randint(minInt, maxInt)
        while tempInt in data:  # no duplicate values
            tempInt = random.randint(minInt, maxInt)
        data.append(tempInt)
    dataString.set(data)

root = Tk()
root.title("Data Structures Visualization")
root.maxsize(1920, 1080)
root.config(bg = "white")

random.seed(time.time())

# Options variables
elementsVar = IntVar(value=10)
minimumVar = IntVar(value=1)
maximumVar = IntVar(value=99)
dataString = StringVar()    # used to update dataViewLabel
insertVar = IntVar(value=1)
removeVar = IntVar(value=1)
findVar = IntVar(value=1)

# Global variables
canvasWidth = 800
canvasHeight = 400
padX = 50
padY = 50
spinboxWidth = 5
# Create all data structures
skipList = SkipList()  # create Skip List
# redBlackTree = RedBlackTree() # create RBT
fibHeap = FibonacciHeap()   # create Fib Heap
linkedList3 = LinkedList()  # DEBUG

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
testButton = Button(buttonWindow, text="Start All", command=lambda : populateAll(data, canvas1, canvas2, canvas3), bg="green", fg="white")
testButton.grid(row=0, column=0, padx=5, pady=5)
# Generate data when button pressed
randomButton = Button(buttonWindow, text="Randomize Data", command=lambda : generateData(int(elementsVar.get()), int(minimumVar.get()), int(maximumVar.get())), bg="blue", fg="white")
randomButton.grid(row=0, column=1, padx=5, pady=5)
# Insert selected value
insertButton = Button(buttonWindow, text="Insert Value", command=lambda : insertIntoAll(int(insertSelect.get()), canvas1, canvas2, canvas3), bg="yellow", fg="black")
insertButton.grid(row=0, column=2, padx=5, pady=5)
# Remove selected value
removeButton = Button(buttonWindow, text="Remove Value", command=lambda : removeFromAll(int(removeSelect.get()), canvas1, canvas2, canvas3), bg="purple", fg="white")
removeButton.grid(row=0, column=3, padx=5, pady=5)
# Find selected value
findButton = Button(buttonWindow, text="Find Value", command=lambda : findInAll(int(findSelect.get()), canvas1, canvas2, canvas3), bg="magenta", fg="white")
findButton.grid(row=0, column=4, padx=5, pady=5)
# Reset button
sortButton = Button(buttonWindow, text="Clear Canvas", command=clearCanvas, bg="red", fg="white")
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
insertLabel = Label(optionWindow, text="Insert", bg="yellow", fg="black")
insertLabel.grid(row=0, column=6, padx=5, pady=5)
# Insert select
insertSelect = Spinbox(optionWindow, from_=minimumVar.get(), to=maximumVar.get(), increment=1, textvariable=insertVar, width=spinboxWidth)
insertSelect.grid(row=1, column=6, padx=5, pady=5)
# Remove label
removeLabel = Label(optionWindow, text="Remove", bg="purple", fg="white")
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
