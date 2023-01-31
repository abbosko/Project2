import math 

class Node:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.child, self.parent, self.left, self.right = None
        
    
class FibonacciHeap:
    min = None
    nodeCount = 0;


    def insert(self,key):
        newNode = Node(key)
        newNode.key = key
        newNode.left = newNode
        newNode.right = newNode
       
        if (self.min != None):
            min.left.right = newNode
            newNode.right = min
            newNode.left = min.left
            min.left = newNode
            if(newNode.key < min.key):
                min = newNode
        else:
            self.min = newNode

    nodeCount+=1;

    #def consolidate():