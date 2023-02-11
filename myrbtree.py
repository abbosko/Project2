import sys
from tkinter import *

#initialize/defining node
class RBNode():
    def __init__(self, key):
        self.key = key
        self.parent = None  #parent node
        self.left = None   #left node
        self.right = None  #right node
        self.color = 1     #1=red , 0 = black
 
 #intialize/defining red black tree
class RedBlackTree():
    def __init__(self):
        self.NULL = RBNode(0)
        self.NULL.color = 0
        self.NULL.right = None
        self.NULL.left = None
        self.root = self.NULL
 
  
 # Preorder
    def preorderHelper(self, node):
        if node != self.NULL:
            #sys.stdout.write(node.key + " ")
            self.preorderHelper(node.left)
            self.preorderHelper(node.right)

    # Inorder
    def inorderHelper(self, node):
        if node != self.NULL:
            self.inorderHelper(node.left)
            #sys.stdout.write(node.key + " ")
            self.inorderHelper(node.right)

    # Postorder
    def postorderHelper(self, node):
        if node != self.NULL:
            self.postorderHelper(node.left)
            self.postorderHelper(node.right)
            #sys.stdout.write(node.key + " ")

    # Search the tree
    def searchTree(self, node, key):
        if node == self.NULL or key == node.key:
            return node
        if key < node.key:
            return self.searchTree(node.left, key)
        return self.searchTree(node.right, key)

    # Balancing the tree after node is removed/deleted
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

 #helps transplant the nodes
    def rbTransplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent
    
 
    #node deletion
    def removeNodeHelper(self, node, key):
        c = self.NULL

        while node != self.NULL: #find node that has particular keyue in it
            if node.key == key:
                c = node         #store in c
 
            if node.key <= key:
                node = node.right
            else:
                node = node.left
 
        if c == self.NULL:       #key not found in the tree
            #print("key not found\n")
            return
 
        b = c
        b_original_color = b.color          #store color
        if c.left == self.NULL:             #if left child is NULL
            a = c.right                     #right child of c to a
            self.rbTransplant(c, c.right)   #transplant node is deleted
        elif (c.right == self.NULL):        #else if right child of c is null
            a = c.left                      #left child of c to a
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
 
    #balance the tree after insertion
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
 
    #printing 
    def printTreeHelper(self, node, indent, last):
        if node != self.NULL:
            #sys.stdout.write(indent)
            if last:
                #sys.stdout.write("R----")
                indent += "     "
            else:
                #sys.stdout.write("L----")
                indent += "|    "
 
            s_color = "RED" if node.color == 1 else "BLACK"
            #print(str(node.key) + "(" + s_color + ")")
            #self.printTreeHelper(node.left, indent, False)
            #self.printTreeHelper(node.right, indent, True)
 
    def preorder(self):
        self.preorderHelper(self.root)

    def inorder(self):
        self.inorderHelper(self.root)

    def postorder(self):
        self.postorderHelper(self.root)

    def searchTrees(self, k):
        return self.searchTree(self.root, k)

    def minimum(self, node):
        while node.left != self.NULL:
            node = node.left
        return node
 
    def maximum(self, node):
        while node.right != self.NULL:
            node = node.right
        return node
 
    def successor(self, a):
        if a.right != self.NULL:
            return self.minimum(a.right)
 
        b = a.parent
        while b != self.NULL and a == b.right:
            a = b
            b = b.parent
        return b
 
    def predecessor(self,  a):
        if (a.left != self.NULL):
            return self.maximum(a.left)
 
        b = a.parent
        while b != self.NULL and a == b.left:
            a = b
            b = b.parent
 
        return b
 
    def leftRotate(self, a):
        b = a.right             #b becomes right child of a
        a.right = b.left        #right child of a becomes left child of b
        if b.left != self.NULL:
            b.left.parent = a
 
        b.parent = a.parent     #parent of b changes to become parent of a
        if a.parent == None:
            self.root = b
        elif a == a.parent.left:
            a.parent.left = b
        else:
            a.parent.right = b
        b.left = a
        a.parent = b
 
    def rightRotate(self, a):
        b = a.left              #b becomes left child of a
        a.left = b.right        #left child of a becomes right child of b
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

    #inserting
    def insert(self, key):
        node = RBNode(key)
        node.parent = None
        node.key = key
        node.left = self.NULL
        node.right = self.NULL
        node.color = 1 #red
 
        b = None #parent
        a = self.root #root
 
        while a != self.NULL: #check if tree is empty
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
            node.color = 0 #black
            return
 
        if node.parent.parent == None:
            return
 
        self.balanceInsertion(node)
 
    def getRoot(self):
        return self.root
 
    def rmvNode(self, key):
        self.removeNodeHelper(self.root, key)
 
    def printHelper(self):
        self.printTreeHelper(self.root, "", True)
 
 
#if __name__ == "__main__":
#    bst = RedBlackTree()
#    total = input("How many numbers?")
#    total = int(total)
#    my_input = []
#    a = 0
#    while a < total:
#        key = input("Enter keys\n")
#        my_input.append(key)
#        bst.insert(my_input[a])
#        a = a + 1
#    #bst.insert(70)
# 
#    bst.print_helper()
#    print("\nAfter deleting an element")
#    bst.rmv_node(my_input[2])
#    bst.print_helper()

    #add remove, #add find
    #change my val to key
    #camel case convention changes