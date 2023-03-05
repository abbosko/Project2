import sys
from tkinter import *
import math
from constants import *

listOfLevels = []
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
    
    def minimum(self, node):
        while node.left != self.NULL:
            node = node.left
        return node
    
    def maximum(self, node):
        while node.right != self.NULL:
            node = node.right
        return node
    
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

# Animation of RBT
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
    above = 2 ** level - 1

    return nodeIndex - above

def animateRBTFind(num, canvas: Canvas, findColor, rbt: RBTree, root, delay):
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
        root.after(delay)
        root.update()

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
            color = 'magenta' if node in findList else 'red' if node.color else 'black'
            outlineColor = outlineColor if node in findList else 'red' if node.color else 'black'
            outlineWidth = 5 if node in findList else 0
            canvas.create_oval(currX-radius, currY-radius, currX+radius, currY+radius, fill=color, outline=outlineColor, width=outlineWidth)
            canvas.create_text(currX, currY, text=node.key, fill="white")