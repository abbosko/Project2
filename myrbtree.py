import sys
from tkinter import *

#initialize/defining node
class RBNode():
    def __init__(self, val):
        self.val = val
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
    def pre_order_helper(self, node):
        if node != NULL:
            sys.stdout.write(node.val + " ")
            self.pre_order_helper(node.left)
            self.pre_order_helper(node.right)

    # Inorder
    def in_order_helper(self, node):
        if node != NULL:
            self.in_order_helper(node.left)
            sys.stdout.write(node.val + " ")
            self.in_order_helper(node.right)

    # Postorder
    def post_order_helper(self, node):
        if node != NULL:
            self.post_order_helper(node.left)
            self.post_order_helper(node.right)
            sys.stdout.write(node.val + " ")

    # Search the tree
    def search_tree(self, node, key):
        if node == NULL or key == node.val:
            return node
        if key < node.val:
            return self.search_tree(node.left, key)
        return self.search_tree(node.right, key)

    # Balancing the tree after node is removed/deleted
    def balance_remove(self, a):
        while a != self.root and a.color == 0:
            if a == a.parent.left:
                s = a.parent.right
                if s.color == 1:
                    s.color = 0
                    a.parent.color = 1
                    self.left_rotate(a.parent)
                    s = a.parent.right
 
                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    a = a.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self.right_rotate(s)
                        s = a.parent.right
 
                    s.color = a.parent.color
                    a.parent.color = 0
                    s.right.color = 0
                    self.left_rotate(a.parent)
                    a = self.root
            else:
                s = a.parent.left
                if s.color == 1:
                    s.color = 0
                    a.parent.color = 1
                    self.right_rotate(a.parent)
                    s = a.parent.left
 
                if s.right.color == 0 and s.right.color == 0:
                    s.color = 1
                    a = a.parent
                else:
                    if s.left.color == 0:
                        s.right.color = 0
                        s.color = 1
                        self.left_rotate(s)
                        s = a.parent.left
 
                    s.color = a.parent.color
                    a.parent.color = 0
                    s.left.color = 0
                    self.right_rotate(a.parent)
                    a = self.root
        a.color = 0

 #helps transplant the nodes
    def __rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent
    
 
    #node deletion
    def remove_node_helper(self, node, val):
        c = self.NULL

        while node != self.NULL: #find node that has particular value in it
            if node.val == val:
                c = node #store in c
 
            if node.val <= val:
                node = node.right
            else:
                node = node.left
 
        if c == self.NULL: #val not found in the tree
            print("Value not found\n")
            return
 
        b = c
        b_original_color = b.color  #store color
        if c.left == self.NULL:     #if left child is NULL
            a = c.right             #right child of c to a
            self.__rb_transplant(c, c.right) #transplant node is deleted
        elif (c.right == self.NULL):     #else if right child of c is null
            a = c.left              #left child of c to a
            self.__rb_transplant(c, c.left)
        else:
            b = self.minimum(c.right)
            b_original_color = b.color
            a = b.right
            if b.parent == c:
                a.parent = b
            else:
                self.__rb_transplant(b, b.right)
                b.right = c.right
                b.right.parent = b
 
            self.__rb_transplant(c, b)
            b.left = c.left
            b.left.parent = b
            b.color = c.color
        if b_original_color == 0:
            self.balance_remove(a)
 
    #balance the tree after insertion
    def balance_insertion(self, k):
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
                        self.right_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
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
                        self.left_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0
 
    #printing 
    def print_tree_helper(self, node, indent, last):
        if node != self.NULL:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
 
            s_color = "RED" if node.color == 1 else "BLACK"
            print(str(node.val) + "(" + s_color + ")")
            self.print_tree_helper(node.left, indent, False)
            self.print_tree_helper(node.right, indent, True)
 
    def preorder(self):
        self.pre_order_helper(self.root)

    def inorder(self):
        self.in_order_helper(self.root)

    def postorder(self):
        self.post_order_helper(self.root)

    def searchTree(self, k):
        return self.search_tree(self.root, k)

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
 
    def left_rotate(self, a):
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
 
    def right_rotate(self, a):
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
    def insert(self, val):
        node = RBNode(val)
        node.parent = None
        node.val = val
        node.left = self.NULL
        node.right = self.NULL
        node.color = 1 #red
 
        b = None #parent
        a = self.root #root
 
        while a != self.NULL: #check if tree is empty
            b = a 
            if node.val < a.val:
                a = a.left
            else:
                a = a.right
 
        node.parent = b
        if b == None:
            self.root = node
        elif node.val < b.val:
            b.left = node
        else:
            b.right = node
 
        if node.parent == None:
            node.color = 0 #black
            return
 
        if node.parent.parent == None:
            return
 
        self.balance_insertion(node)
 
    def get_root(self):
        return self.root
 
    def rmv_node(self, val):
        self.remove_node_helper(self.root, val)
 
    def print_helper(self):
        self.print_tree_helper(self.root, "", True)
 
 
if __name__ == "__main__":
    bst = RedBlackTree()
    total = input("How many numbers?")
    total = int(total)
    my_input = []
    a = 0
    while a < total:
        val = input("Enter values\n")
        my_input.append(val)
        bst.insert(my_input[a])
        a = a + 1
    #bst.insert(70)
 
    bst.print_helper()
    print("\nAfter deleting an element")
    bst.rmv_node(my_input[2])
    bst.print_helper()

    #add remove, #add find