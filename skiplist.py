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
        if nodeToRemove != None:
            for i in range(len(nodeToRemove.next)):
                path[i].next[i] = nodeToRemove.next[i]
    
    # returns list of nodes in row r
    def getRow(self, r):

        # return None if r > height of SkipList
        if r > len(self.head.next) - 1:
            return None
        
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
        if len(self.head.next) == 0:
            return None

        # call getRow for each row in skip list and add to rows list.
        rows = []
        for i in range(len(self.head.next)):
            rows.append(self.getRow(i))
        return rows

# def main():
#     sl = SkipList()
#     for i in range (1, 51):
#         sl.insert(i)
#         print(str(i) + " inserted at row " + str(len(sl.find(i).next) - 1))
    
#     print()
#     print()

#     for i in range (0, 11):
#         temp = sl.getRow(i)
#         if temp != None:
#             print("Row " + str(i), end=': ')
#             for node in temp:
#                 print(str(node.key), end=' ')
#             print()

#     print()
#     print()

#     rows = sl.getRows()
#     for i in range(len(rows)):
#         print("Row " + str(i), end=': ')
#         for node in rows[i]:
#             print(str(node.key), end=' ')
#         print()

# if __name__ == "__main__":
#     main()
