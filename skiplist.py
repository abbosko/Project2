import random
from tkinter import *

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

    # inserts a new node with the given key
    def insert(self, key):
        # creates a new node with the given key
        height = pickHeight()
        print("inserting " + str(key) + " at height " + str(height))
        newNode = SkipNode(key, height)
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
        # adjust length of head's next pointers
        while None in self.head.next:
            self.head.next.remove(None)


    # returns list of nodes in row r
    def getRow(self, r):
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
                print("adding " + str(i) + ", " + str(column) + " to list")
                ptr = ptr.next[i]
            # -1 indicates Head
            if ptr.key == None:
                column = -1
            else:
                column = rows[i].index(ptr)
            fullPath.append((i, column))
            print("adding " + str(i) + ", " + str(column) + " to list")
        
        if ptr.next[0] and ptr.next[0].key == key:
            fullPath.append((0, rows[0].index(ptr.next[0])))
        # return the FULL path taken down the list
        # tuple of (row, column)
        return fullPath

# def main():
#     sl = SkipList()
#     for i in range (1, 50):
#         sl.insert(i)
#     fullPath = sl.getFullPath(40)
#     print(fullPath)

# if __name__ == "__main__":
#     main()