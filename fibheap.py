import math 

class FibNode:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = self.left = self.right= self.child = None
        self.color = 'N'     # for find
        self.mark = False    #flag for find 

    
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

    def addToTree(self, bigger, smaller):   # when consolidating, this adds the smaller tree to the bigger tree
        self.removeFromRootList(bigger)
        if( smaller.right == smaller):
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
        smaller.degree+=1
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

        #if only one child 
        if (parent.child == parent.child.right):
            parent.child = None
        
        #when found node cut it out by reset ptrs
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

        #add it to root list
        self.addToRootList(newNode)

        #set as new min if smallest or no min
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
        

        if (self.min == None):
            print("Heap empty, can't extract")

        else:

            oldMin = self.min
            if(oldMin.child != None):
                # if the min has children
                #for every child of old minimum add to root list
                children = [x for x in self.iterate(oldMin.child)]

                for i in children:
                    self.addToRootList(i)
     
                    if( i.key <  self.min.key):
                        self.min = i
                    # self.removeFromChildList(children[i])
                    i.parent = None
    

            self.removeFromRootList(oldMin)
            self.min = oldMin.right
            if( oldMin == oldMin.right):

                    self.min = None
                    
            else: 
                self.min = oldMin.right
                self.consolidate()
            self.nodeCount-=1

            

    def consolidate(self):
        aux = [None] * int(math.log(self.nodeCount) * 2)    # I found this online idk
        # aux = ((math.frexp(self.nodeCount)[1] - 1) + 1) * [None]

        #get root list
        array = [node for node in self.iterate(self.min)]

     
        while array != []:
            first = array[0]
            degree = first.degree
            array.remove(first)
            while aux[degree] is not None:
                #if already have tree of that degree
                second = aux[degree]
                #grab that value 
                if first.key > second.key: # this is to ensure that the second is larger than the first
                    temp = first
                    first = second
                    second = temp
                self.addToTree(second, first) # link tree
                aux[degree] = None #reset to 0
                degree += 1    
            aux[degree] = first
        self.min = None
        # for i in array:
        #    self.addToRootList(i)
        # self.min = None
        # Find min node
       
        for i in aux:
            if i is not None:
  
                if self.min is None or i.key < self.min.key:
 
                    self.min = i

    
    def cut(self, node, parent):
        #no longer a child so remove from child list 
        self.removeFromChildList(parent, node)
        parent.degree -=1
        self.addToRootList(node)
        node.parent = None
        node.mark = False
 
    
    def cascadeCut(self, node):
        ptr = node.parent
        if (ptr != None):
            if (node.mark == False):
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
            if (ptr.right.color != 'Y'):
                self.find(start.right, val);
        ptr.color = 'N'
        
       
    
    def delete(self, val):

        if( self.min == None):
            print("Error: Heap Empty")
        
        elif (self.min.key == val):
            self.extract_min()

        else:
            self.finder = None
            self.find(self.min, val)
            node = self.finder
            
       
            if (node == None):
                print("not found")
            else:
                # Decreasing the value of the node to new min
                self.decrease_key(node, self.min.key - 1 )
                # Calling Extract_min function to delete node
                self.extract_min()

 
    def display(self):
        ptr1 = self.min
        if (ptr1 == None):
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
          



'''## for testing purposes
if __name__ == '__main__':
    fib_heap = FibonacciHeap()
    fib_heap.insert(7)
    fib_heap.insert(30)
    fib_heap.insert(24)
    fib_heap.insert(26)
    fib_heap.insert(35)
    fib_heap.insert(46)
    fib_heap.insert(23)
    fib_heap.insert(17)
    fib_heap.insert(3)
    fib_heap.insert(8)

    fib_heap.display()
    
    fib_heap.delete(26)
    fib_heap.display()

    fib_heap.delete(8)
    fib_heap.display()

    fib_heap.delete(35)
    fib_heap.display()

    fib_heap.delete(17)
    fib_heap.display()
    
    fib_heap.delete(3)
    fib_heap.display()

    fib_heap.delete(23)
    fib_heap.display()
   

# insert, delete, and find '''