# CS 470 Team 2, February 2023
# Skip List - Sam Gaines and Scott Ratchford
# Red-Black Tree -
# Fibbonaci Heap - 
# Animations - Scott Ratchford

from tkinter import *
import random
import time
import math

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
    def animateFind(self, key, canvas: Canvas, color="blue", delay=True):
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
    
    def drawSkipList(self, canvas: Canvas):
        canvas.delete("all")
        global padX
        global padY
        allRows = self.getRows()
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
                        node.drawSkipNode(canvas, element[1], currY, nodeColor)
                        nodeMatrix[index][bottomIndex] = (node, currX, currY)
                        found = True
                if(not found):  # found is a bool, so duplicates do not yet appear
                    currX = (((getCanvasX(canvas) - 2 * padX) / (len(allRows[0]) + 2)) * (rowIndex + 2)) + padX  # for now, currX is determined per row
                    node.drawSkipNode(canvas, currX, currY, nodeColor)
                    nodeMatrix[rowIndex][bottomIndex] = (node, currX, currY)

# Fib Heap Code

# fib heap node class
class FibNode:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = self.left = self.right = self.child = None
        self.color = 'N'     # for find
        self.mark = False    # flag for find 
        self.k = 'N'
    
    def drawFibNode(self, canvas: Canvas, X, Y, color, textColor):
        radius = calculateRadius(self.key)
        canvas.create_oval(X-radius, Y-radius, X+radius, Y+radius, fill=color)
        canvas.create_text(X, Y, text=str(self.key), fill=textColor)

# fib heap class
class FibonacciHeap:
    def __init__(self):
        self.min = None
        self.nodeCount = 0
        self.finder = None
        self.findList = []
    
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
        # get root list
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
        self.findList.append(ptr)
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
        self.findList.clear()
        if(self.min.key == val and self.min != None):
            self.findList.append(self.min)
            self.extract_min()
        else:
            self.finder = None
            self.find(self.min, val)
            node = self.finder
            if(node != None):
                # Decreasing the value of the node to new min
                self.decrease_key(node, self.min.key - 1)
                # Calling Extract_min function to delete node
                self.extract_min()
    
    def drawFibHeap(self, canvas): 
        canvas.delete("all")
        rootList = [node for node in self.iterate(self.min)]
        height = max(node.degree for node in rootList)
        rootOffset = ((canvasWidth - 100)) / (len(rootList) + height)
        yInc = (canvasHeight - 100) / (height + 1)
        self.drawFib(self.min, canvas, rootOffset, 50, rootOffset, yInc, rootList)

    def animateFind(self, canvas, num): 
        canvas.delete("all")
        self.drawFibHeap(canvas)
        self.findList.clear()
        self.find(self.min, num)
        
        rootList = [node for node in self.iterate(self.min)]
        height = max(node.degree for node in rootList)
        rootOffset = ((canvasWidth - 100)) / (len(rootList) + height)
        yInc = (canvasHeight - 100) / (height + 1)
        self.highlightFind(self.min, canvas, rootOffset, 50, rootOffset, yInc, rootList)

    def drawFib(self, node, canvas, x, y, rootOffset, yInc, rootList):
        if(node == self.min):
            color = 'cyan'
            textColor = "black"
        else:
            color = nodeColor
            textColor = "black"
        node.drawFibNode(canvas, x, y, color, textColor)
        radius = calculateRadius(node.key)
        totalSpace = rootOffset/2
        offset = -totalSpace * (node.degree - 1) / 2
        child = node.child
        for childTree in range(node.degree):
            canvas.create_line(x, y + radius, x + offset, y + yInc)
            self.highlightFind(child, canvas, x + offset, y + yInc, rootOffset, yInc, rootList)
            # offset from siblings
            if(child != node.child.left):
                offset = offset * (childTree)
            if(child.right == node.child.left):
                offset = offset * (childTree) + 50
            child = child.right
        #rootList
        if node in rootList and node.right != self.min:
            canvas.create_line(x + radius, y, x + rootOffset - radius, y, arrow=LAST)
            canvas.create_line(x + radius, y, x + rootOffset - radius, y, arrow=FIRST)
            self.highlightFind(node.right, canvas, x + rootOffset, y, rootOffset, yInc, rootList)

    def highlightFind(self, node, canvas, x, y, rootOffset, yInc, rootList):
        if(node in self.findList):
            color = findColor
            textColor = "white"
            node.drawFibNode(canvas, x, y, color, textColor)
            root.after(delaySelect.get())   # delay
            root.update()
        radius = calculateRadius(node.key)
        totalSpace = rootOffset/2
        offset = -totalSpace * (node.degree - 1) / 2
        child = node.child
        for childTree in range(node.degree):
            canvas.create_line(x, y + radius, x + offset, y + yInc)
            self.drawFib(child, canvas, x + offset, y + yInc, rootOffset, yInc, rootList)
            # offset from siblings
            if(child != node.child.left):
                offset = offset * (childTree)
            if(child.right == node.child.left):
                offset = offset * (childTree) + 50
            child = child.right
        #rootList
        if node in rootList and node.right != self.min:
            canvas.create_line(x + radius, y, x + rootOffset - radius, y, arrow=LAST)
            canvas.create_line(x + radius, y, x + rootOffset - radius, y, arrow=FIRST)
            self.drawFib(node.right, canvas, x + rootOffset, y, rootOffset, yInc, rootList)

# Red Black Tree Code

# red black tree node class
class RBTreeNode:
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1       # 1=red, 0=black

# red black tree class
class RBTree:
    def __init__(self):
        self.NULL = RBTreeNode(0)
        self.NULL.color = 0
        self.NULL.right = None
        self.NULL.left = None
        self.root = self.NULL
# Preorder

    def leftRotate(self, a):
        b = a.right             # b becomes right child of a
        a.right = b.left        # right child of a becomes left child of b
        if b.left != self.NULL:
            b.left.parent = a
        b.parent = a.parent     # parent of b changes to become parent of a
        if a.parent == None:
            self.root = b
        elif a == a.parent.left:
            a.parent.left = b
        else:
            a.parent.right = b
        b.left = a
        a.parent = b

    def rightRotate(self, a):
        b = a.left              # b becomes left child of a
        a.left = b.right        # left child of a becomes right child of b
        if b.right != self.NULL:
            b.right.parent = a
        b.parent = a.parent
        if a.parent == None:
            self.root = b
        elif a == a.parent.right:
            a.parent.right = b
        else:
            a.parent.left = b
        b.right = a
        a.parent = b

    def rbTransplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # Node Deletion
    def remove(self, key):
        self.removeNodeHelper(self.root, key)

    def removeNodeHelper(self, node, key):
        c = self.NULL
        while node != self.NULL: # find node that has particular keyue in it
            if node.key == key:
                c = node         # store in c
            if node.key <= key:
                node = node.right
            else:
                node = node.left
        if c == self.NULL:       # key not found in the tree
            return
 
        b = c
        b_original_color = b.color          # store color
        if c.left == self.NULL:             # if left child is NULL
            a = c.right                     # right child of c to a
            self.rbTransplant(c, c.right)   # transplant node is deleted
        elif (c.right == self.NULL):        # else if right child of c is null
            a = c.left                      # left child of c to a
            self.rbTransplant(c, c.left)
        else:
            b = self.minimum(c.right)
            b_original_color = b.color
            a = b.right
            if b.parent == c:
                a.parent = b
            else:
                self.rbTransplant(b, b.right)
                b.right = c.right
                b.right.parent = b
 
            self.rbTransplant(c, b)
            b.left = c.left
            b.left.parent = b
            b.color = c.color
        if b_original_color == 0:
            self.balanceRemove(a)

    def balanceRemove(self, a):
        while a != self.root and a.color == 0:
            if a == a.parent.left:
                s = a.parent.right
                if s.color == 1:
                    s.color = 0
                    a.parent.color = 1
                    self.leftRotate(a.parent)
                    s = a.parent.right
 
                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    a = a.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self.rightRotate(s)
                        s = a.parent.right
 
                    s.color = a.parent.color
                    a.parent.color = 0
                    s.right.color = 0
                    self.leftRotate(a.parent)
                    a = self.root
            else:
                s = a.parent.left
                if s.color == 1:
                    s.color = 0
                    a.parent.color = 1
                    self.rightRotate(a.parent)
                    s = a.parent.left
 
                if s.right.color == 0 and s.right.color == 0:
                    s.color = 1
                    a = a.parent
                else:
                    if s.left.color == 0:
                        s.right.color = 0
                        s.color = 1
                        self.leftRotate(s)
                        s = a.parent.left
 
                    s.color = a.parent.color
                    a.parent.color = 0
                    s.left.color = 0
                    self.rightRotate(a.parent)
                    a = self.root
        a.color = 0

    # Node Insertion
    def insert(self, key):
        node = RBTreeNode(key)
        node.parent = None
        node.key = key
        node.left = self.NULL
        node.right = self.NULL
        node.color = 1 # red
 
        b = None # parent
        a = self.root # root
 
        while a != self.NULL: # check if tree is empty
            b = a 
            if node.key < a.key:
                a = a.left
            else:
                a = a.right
 
        node.parent = b
        if b == None:
            self.root = node
        elif node.key < b.key:
            b.left = node
        else:
            b.right = node
 
        if node.parent == None:
            node.color = 0 # black
            return
 
        if node.parent.parent == None:
            return
 
        self.balanceInsertion(node)

    def balanceInsertion(self, k):
        while k.parent.color == 1:                  #parent of k is red
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.rightRotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.leftRotate(k.parent.parent)
            else:
                u = k.parent.parent.right
 
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.leftRotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.rightRotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0
    # Search the tree
    def searchTree(self, node, key):
        if node == self.NULL or key == node.key:
            return node
        if key < node.key:
            return self.searchTree(node.left, key)
        return self.searchTree(node.right, key)

    # Misc.

    def getLevels(self):
        # Initialize list to return
        listOfLevels = []
        def getLevelsHelper(node, l):
            # If node's value is 0 (at leaf), return
            if node.key == 0:
                return
            # If first time entering level, initalize and append the level's list to main list
            if l >= len(listOfLevels):
                list = []
                listOfLevels.append(list)
            # Append node to the level's list
            listOfLevels[l].append(node)
            getLevelsHelper(node.left, l+1)
            getLevelsHelper(node.right, l+1)
        getLevelsHelper(self.root, 0)

        return listOfLevels
    
    def drawRBTree(self, canvas: Canvas, findList=[], findColor = 'magenta'):
        canvas.delete("all")
        allLevels = self.getLevels()

        # Draw the lines first
        # For each level
        for degreeIndex, level in enumerate(allLevels):
            # For each value in level
            currDegree = degreeIndex
            currY = (((getCanvasY(canvas) + (padY * 2)) / (len(allLevels) + 1)) * (currDegree + 1)) - padY
            for node in allLevels[degreeIndex]:
                levelIndex = findLevelIndex(self, node)
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
                levelIndex = findLevelIndex(self, node)
                currDegree = degreeIndex
                currX = padX + (((getCanvasX(canvas) - (padX * 2)) / (math.pow(2, currDegree) + 1)) * (levelIndex + 1))
                radius = calculateRadius(node.key)
                color = findColor if node in findList else 'red' if node.color else 'black'
                canvas.create_oval(currX-radius, currY-radius, currX+radius, currY+radius, fill=color)
                canvas.create_text(currX, currY, text=node.key, fill="white")
            
    def animateFindRBT(self, num, canvas: Canvas, findColor):
        nodesTraversed = []
        current = self.root

        while (current != None and current != self.NULL):
            nodesTraversed.append(current)

            if current.key == num:
                break
            elif current.key > num:
                current = current.left
            else:
                current = current.right
        
        self.drawRBTree(canvas, nodesTraversed, findColor)


# Same idea as calculation of index of children from binary heap represented as an array
def findNodeIndex(tree, node):
    if node.parent == None or node.parent == tree.NULL:
        return 0
    
    if node == node.parent.left:
        return 2 * findNodeIndex(tree, node.parent) + 1
    else:
        return 2 * findNodeIndex(tree, node.parent) + 2

def findLevelIndex(tree, node):
    nodeIndex = findNodeIndex(tree, node)
    level = int(math.log2(1 + nodeIndex))
    above = 2**level - 1

    return nodeIndex - above


# Calculates a radius such that the text within will fit into the circle
def calculateRadius(key):
    if(10 + (len(str(key))) * 1.2 > 12.4):
        return 10 + (len(str(key))) * 1.2   # determine radius of node based on length of the string
    else:
        return 12.4

# Animates the insertion of every data point into each of the three data structures
def populateAll(data, canvas1: Canvas, canvas2: Canvas, canvas3: Canvas):
    global skipList
    global fibHeap
    global redBlackTree
    
    # reset data structures
    skipList = SkipList()
    redBlackTree = RBTree()
    fibHeap = FibonacciHeap()

    # insert all elements in list
    for index, num in enumerate(data):
        # skip list
        if(index != 0):
            skipList.animateFind(num, canvas1, insertColor, True)    # draw with delays
            skipList.insert(num)
            skipList.animateFind(num, canvas1, insertColor, False)   # redraw with no delays
        else:
            skipList.insert(num)
        # fib heap
        fibHeap.insert(num)
        fibHeap.drawFibHeap(canvas2)
        # red black tree
        redBlackTree.insert(num)
        redBlackTree.drawRBTree(canvas3)

        root.after(delaySelect.get())   # delay after every data structure is updated
        root.update()

    skipList.drawSkipList(canvas1)
    fibHeap.drawFibHeap(canvas2)
    # rbt

# Animates the insertion of a specified data point into each of the three data structures
def insertIntoAll(num, canvas1: Canvas, canvas2: Canvas, canvas3: Canvas):
    global skipList
    global fibHeap
    global redBlackTree

    # do not insert duplicates
    if(skipList.find(num) != None):
        return

    # skip list
    skipList.animateFind(num, canvas1, insertColor, True)    # draw with delays
    skipList.insert(num)
    skipList.animateFind(num, canvas1, insertColor, False)   # redraw with no delays
    fibHeap.insert(num)
    # fib heap
    fibHeap.drawFibHeap(canvas2)
    redBlackTree.insert(num)
    redBlackTree.drawRBTree(canvas3)
    root.after(delaySelect.get())
    root.update()

    # rbt

    root.after(delaySelect.get())   # delay after every data structure is updated
    root.update()

# Animates the removal of a specified data point from each of the three data structures
def removeFromAll(num, canvas1: Canvas, canvas2: Canvas, canvas3: Canvas):
    global skipList
    global fibHeap
    global redBlackTree

    # skip list
    skipList.animateFind(num, canvas1, removeColor, True)    # draw with delays
    skipList.remove(num)
    root.after(delaySelect.get())
    root.update()
    skipList.animateFind(num, canvas1, removeColor, False)    # draw with delays
    # fib heap
    fibHeap.findList.clear()
    fibHeap.delete(int(num))
    fibHeap.findList.clear()
    fibHeap.drawFibHeap(canvas2)
    redBlackTree.remove(num)
    redBlackTree.drawRBTree(canvas3)

    root.after(delaySelect.get())
    root.update()
    skipList.animateFind(num, canvas1, removeColor, False)    # draw with delays

    root.after(delaySelect.get())   # delay after every data structure is updated
    root.update()

# Animates the search for a specified data point in each of the three data structures
def findInAll(num, canvas1: Canvas, canvas2: Canvas, canvas3: Canvas):
    global skipList
    # global fibHeap
    global redBlackTree

    skipList.animateFind(num, canvas1, findColor, True)
    redBlackTree.animateFindRBT(num, canvas3, findColor)
    root.update()

    fibHeap.animateFind(canvas2, num)
    root.update()

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
randomButton = Button(buttonWindow, text="Randomize Data", command=lambda : generateData(int(elementsVar.get()), int(minimumVar.get()), int(maximumVar.get())), bg=nodeColor, fg="black")
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
