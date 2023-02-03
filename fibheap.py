import math 


class Node:
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

    def addToTree(self, parent, node):   # when consolidating, this adds the smaller tree to the bigger tree
        self.removeFromRootList(parent)
        parent.left = parent
        parent.right = parent
        self.addToChildList(node, parent)
        node.degree +=1 
        parent.parent = node
        parent.mark = False
        

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
            parent.child == None
        
        #when found node cut it out by reset ptrs
        elif parent.child == node:
            parent.child = node.right
            node.right.parent = parent
        
        # cut out
        node.left.right = node.right
        node.right.left = node.left


    def insert(self, key):

        # make new node, set pointers to itself for doubly linked
        newNode = Node(key)
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
        oldMin = self.min
    
        if (self.min == None):
            print("Heap empty, can't extract")

        else:
            if(oldMin.child != None):
                # if the min has children
                #for every child of old minimum add to root list
                children = [x for x in self.iterate(oldMin.child)]
                for i in range(0, len(children)):
                    self.addToRootList(children[i])
                    # self.removeFromChildList(children[i])
                    children[i].parent = None
                

            self.removeFromRootList(oldMin)
            if( oldMin == oldMin.right):
                    self.min = None
                    
            else: 
                self.min = oldMin.right
                self.consolidate()
            self.nodeCount-=1

            

    def consolidate(self):
        aux = [None] * int(math.log(self.nodeCount) * 2)    # I found this online idk
        # aux = ((math.frexp(self.nodeCount)[1] - 1) + 1) * [None]
        array = [node for node in self.iterate(self.min)]
        while array != []:
            first = array[0]
            degree = first.degree
            array.remove(first)
            while aux[degree] is not None:
                second = aux[degree]
                if first.key > second.key:  # this is to ensure that the second is larger than the first
                    temp = first
                    first = second
                    second = temp
                self.addToTree(second, first)
                aux[degree] = None
                degree += 1
            aux[degree] = first
        # for i in array:
        #    self.addToRootList(i)
        # self.min = None
        # Find min node
        for i in aux:
            if i is not None:
                if i.key < self.min.key:
                    print(i)
                    self.min = i

    
    def cut(self, node, parent):
        #no longer a child so remove from child list 
        self.removeFromChildList(parent, node)
        parent.degree -+1
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
        found = False
        ptr.color = 'Y'


        if(ptr.key == val):
            found == True
            ptr.color = 'N'
            self.finder = ptr
            return 

        if(found == False):
            if(ptr.child != None):
                self.find(start.child, val)
            if (ptr.right.color != 'Y'):
                self.find(start.right, val);

        
       
    
    def delete(self, val):
        if( self.min == None):
            print("Error: Heap Empty")
        
        elif (self.min.key == val):
            self.extract_min()

        else:
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
          
    

'''
## for testing purposes
if __name__ == '__main__':
    fib_heap = FibonacciHeap()
    fib_heap.insert(7)
    fib_heap.insert(30)
    fib_heap.insert(24)
    
  
    #fib_heap.consolidate()
    #fib_heap.display()

    # fib_heap.extract_min()
    # print(" extracting min")
    # fib_heap.display()

   
    fib_heap.insert(26)
    fib_heap.insert(35)
    fib_heap.insert(46)
    fib_heap.insert(23)
    fib_heap.insert(17)
    fib_heap.insert(3)
    fib_heap.insert(18)

   
    
    # fib_heap.extract_min()
    # print(" extracting min: ", fib_heap.extract_min())
    fib_heap.display()

    print("deleting 46")

    fib_heap.delete(46)
    fib_heap.display()


   
    ## fib_heap.insert(2)
    # fib_heap.insert(8)
    # fib_heap.insert(5)
    # fib_heap.insert(2)
    # fib_heap.insert(8)


# insert, delete, and find '''