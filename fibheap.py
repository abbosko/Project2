import math 
from tkinter import *
import time
from constants import *

class FibNode:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = self.left = self.right = self.child = None
        self.color = 'N'     # for find
        self.mark = False    # flag for find 

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

    def extract_min(self, canvas, delay, root, color):
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
            drawFibHeap(canvas, self, color)
            root.after(delay)
            root.update()
            self.min = oldMin.right
            if(oldMin == oldMin.right):
                self.min = None
            else: 
                self.min = oldMin.right
                self.consolidate(canvas, root, delay, color)
            self.nodeCount -= 1

    def consolidate(self, canvas, root, delay, color):
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
                # animate
                drawFibHeap(canvas, self, color)
                root.after(delay)   # delay
                root.update()
                aux[degree] = None # reset to 0
                degree += 1    
            aux[degree] = first
        self.min = None
        # Find min node
        for i in aux:
            if i is not None:
                if self.min is None or i.key < self.min.key:
                    self.min = i
    
    def cut(self, node, parent, canvas, root, delay, color):
        # no longer a child so remove from child list 
        self.removeFromChildList(parent, node)
        parent.degree -= 1
        self.addToRootList(node)
        drawFibHeap(canvas, self, color)
        root.after(delay)
        root.update()
        node.parent = None
        node.mark = False
    
    def cascadeCut(self, node, canvas, root, delay, color):
        ptr = node.parent
        if(ptr != None):
            if(node.mark == False):
                drawFibHeap(canvas, self, color)
                root.after(delay)
                root.update()
                node.mark = True
            else:
                self.cut(node, ptr, canvas, root, delay, color)
                self.cascadeCut(ptr, canvas, root, delay, color)

    # decrease key used for delete
    def decrease_key(self, node, val, canvas, root, delay, color):
        # not decreasing
        if val > node.key:
            return None
        # set new key value to node
        node.key = val
        parent = node.parent
        # if node is now smaeller than its parent, cut and refactor
        if parent != None and node.key < parent.key:
            self.cut(node, parent, canvas, root, delay, color)
            self.cascadeCut(parent, canvas, root, delay, color)
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

    def delete(self, val, canvas, root, delay, color):
        self.findList.clear()
        if(self.min.key == val and self.min != None):
            # self.findList.append(self.min)
            self.extract_min(canvas, delay, root, color)
        else:
            self.finder = None
            self.find(self.min, val)
            node = self.finder
            if(node != None):
                # Decreasing the value of the node to new min
                self.decrease_key(node, self.min.key - 1, canvas, root, delay, color)
                # Calling Extract_min function to delete node
                self.extract_min(canvas, delay, root, color)

       
def drawFibNode(canvas: Canvas, X, Y, color, textColor, node):
    radius = calculateRadius(node.key)
    canvas.create_oval(X-radius, Y-radius, X+radius, Y+radius, fill=color)
    canvas.create_text(X, Y, text=str(node.key), fill=textColor)

def drawFibHeap(canvas, fibHeap: FibonacciHeap, nodeColor): 
    canvas.delete("all")
    rootList = [node for node in fibHeap.iterate(fibHeap.min)]
    height = max(node.degree for node in rootList)
    rootOffset = ((800 - 100)) / (len(rootList) + height)
    yInc = (400 - 100) / (height + 1)
    drawFib(fibHeap.min, canvas, rootOffset, 50, rootOffset, yInc, rootList, fibHeap, nodeColor)

def animateFibFind(canvas, num, fibHeap: FibonacciHeap, root, delay, color="magenta"): 
    canvas.delete("all")
    drawFibHeap(canvas, fibHeap, "yellow")
    fibHeap.findList.clear()
    fibHeap.find(fibHeap.min, num)
    findIdx = 0
    for idx, node in enumerate(fibHeap.findList):
        if node.key == num:
            findIdx = idx
            break
    fibHeap.findList = fibHeap.findList[0:findIdx + 1]

    rootList = [node for node in fibHeap.iterate(fibHeap.min)]
    height = max(node.degree for node in rootList)
    rootOffset = ((800 - 100)) / (len(rootList) + height)
    yInc = (400 - 100) / (height + 1)
    highlightFibFind(fibHeap.min, canvas, rootOffset, 50, rootOffset, yInc, rootList, color, fibHeap, root, delay)

def drawFib(node, canvas, x, y, rootOffset, yInc, rootList, fibHeap: FibonacciHeap, nodeColor):
    if(node == fibHeap.min):   # head
        color = "cyan"
    else:
        color = nodeColor
        if(node.mark == True):
            color = 'green'
    textColor = "black"
    drawFibNode(canvas, x, y, color, textColor, node)
    radius = calculateRadius(node.key)
    totalSpace = rootOffset / 2
    offset = -totalSpace * (node.degree - 1) / 2
    child = node.child
    for childTree in range(node.degree):
        canvas.create_line(x, y + radius, x + offset, y + yInc)
        drawFib(child, canvas, x + offset, y + yInc, rootOffset, yInc, rootList, fibHeap, nodeColor)
        # offset from siblings
        if(child != node.child.left):
            offset = offset * (childTree) + 10
        if(child.right == node.child.left):
            offset = offset * (childTree) + 50
        child = child.right
    # rootList
    if node in rootList and node.right != fibHeap.min:
        canvas.create_line(x + radius, y, x + rootOffset - radius, y, arrow=LAST)
        canvas.create_line(x + radius, y, x + rootOffset - radius, y, arrow=FIRST)
        drawFib(node.right, canvas, x + rootOffset, y, rootOffset, yInc, rootList, fibHeap, nodeColor)

def highlightFibFind(node, canvas: Canvas, x, y, rootOffset, yInc, rootList, color, fibHeap: FibonacciHeap, root, delay):
    if(node in fibHeap.findList):
        textColor = "white"
        drawFibNode(canvas, x, y, color, textColor, node)
        root.after(delay)   # delay
        root.update()
    totalSpace = rootOffset/2
    offset = -totalSpace * (node.degree - 1) / 2
    child = node.child
    for childTree in range(node.degree):
        highlightFibFind(child, canvas, x + offset, y + yInc, rootOffset, yInc, rootList, color, fibHeap, root, delay)
        # offset from siblings
        if(child != node.child.left):
            offset = offset * (childTree) + 10
        if(child.right == node.child.left):
            offset = offset * (childTree) + 50
        child = child.right
    #rootList
    if node in rootList and node.right != fibHeap.min:
        highlightFibFind(node.right, canvas, x + rootOffset, y, rootOffset, yInc, rootList, color, fibHeap, root, delay)