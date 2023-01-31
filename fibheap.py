import math 


class Node:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = self.left = self.right = None
        self.child = []     # Setting as array makes consolidating easier

    def addToTree(self, smaller):   # when consolidating, this adds the smaller tree to the bigger tree
        self.child.append(smaller)
        self.degree += 1
        
    
class FibonacciHeap:
    def __init__(self):
        self.min = None
        self.nodeCount = 0

    def insert(self, key):
        newNode = Node(key)
        newNode.key = key
        newNode.left = newNode
        newNode.right = newNode
       
        if self.min is not None:
            self.min.left.right = newNode
            newNode.right = min
            newNode.left = self.min.left
            self.min.left = newNode
            if newNode.key < self.min.key:
                self.min = newNode
        else:
            self.min = newNode

        self.nodeCount += 1

    def find_min(self):
        return self.min.key

    # This iterates through the doubly linked list starting at min, helps with consolidate
    def iterate(self):
        node = end = self.min
        stop = False
        while True:
            if node == end and stop is True:  # means it is back at the starting point
                break
            elif node == end:
                stop = True
            yield node
            node = node.left

    def consolidate(self):
        aux = [None] * int(math.log(self.nodeCount) + 2)    # I found this online idk
        array = [node for node in self.iterate()]
        while array:
            first = array[0]
            degree = first.degree
            array.remove(first)
            while aux[degree] is not None:
                second = aux[degree]
                if first.key > second.key:  # this is to ensure that the second is larger than the first
                    temp = first
                    first = second
                    second = temp
                second.addToTree(first)
                aux[degree] = None
                degree += 1
            aux[degree] = first

        # Find min node
        for i in aux:
            if i is not None:
                if i.key < self.min.key:
                    self.min = i


# for testing purposes
# if __name__ == '__main__':
#     fib_heap = FibonacciHeap()
#     fib_heap.insert(2)
#     fib_heap.insert(4)
#     fib_heap.insert(1)
#     fib_heap.insert(17)
#     print(fib_heap.find_min())
#     fib_heap.consolidate()


