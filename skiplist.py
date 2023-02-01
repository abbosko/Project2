import random

# picks the height for a node
def pickHeight():
    height = 1
    while (random.choice([True, False])):
        height += 1
    return height
        
class Node:
    def __init__(self, key=None, height=0):
        self.key = key
        self.next = [None] * height

class SkipList:

    def __init__(self):
        self.head = Node()

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
    def search(self, key, path=None):
        
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
        newNode = Node(key, pickHeight())
        
        # adds another level of pointer to the head, if necessary
        while len(self.head.next) < len(newNode.next):
            self.head.next.append(None)
        
        # inserts node and updates pointers in each height level the node reaches
        # doesn't insert duplicates... rip
        path = self.getPath(key)
        if self.search(key, path) == None:
            for i in range(len(newNode.next)):
                newNode.next[i] = path[i].next[i]
                path[i].next[i] = newNode
    
    # removes a node with the given key
    def remove(self, key):

        # updates pointers around each height level the node is in
        path = self.getPath(key)
        nodeToRemove = self.search(key, path)
        if nodeToRemove != None:
            for i in range(len(nodeToRemove.next)):
                path[i].next[i] = nodeToRemove.next[i]

# def main():
#     sl = SkipList()
#     for i in range(10):
#         newInt = random.randint(0, 50)
#         sl.insert(newInt)
#         print("inserting " + str(newInt))

#     print()

#     for i in range(50):
#         found = sl.search(i)
#         if (found == None):
#             print(str(i) + " not found")
#         else:
#             print(str(found.key) + " found at level " + str(len(found.next) - 1))
    
#     print()

#     for i in range(len(sl.head.next)):
#         print("Level " + str(i))
#         temp = sl.head.next[i]
#         while (temp != None):
#             print(temp.key)
#             temp = temp.next[i]

# if __name__ == "__main__":
#     main()