## CS 470 Project 2
Scott Ratchford, Sam Gaines, Abbie Bosko, Audrey Kim, Summer Hawkins, Kevin Lee

### Project Description
This project compares three data structures: 
  1. Red-Black Trees
  2. Fibonacci Heaps
  3. Skip Lists

The purpose of this project is to compare the three data structures on the following operations:
  * Insert
  * Find
  * Delete

Python and Tkinter were used for the implementation of the comparison.

### Overview
To begin, run tripleVisualization.py. Once the GUI has opened, the user has the option to choose how many elements they want to add to the data structures using the "elements" spinbox. The default value for this is 10.

Once element size has been chosen, the user then can then select to randomize data with the corresponding buttom to generate a new dataset.

After randomizing data, the "Start All" button begins inserting the dataset into each data structure.

The spinbox **Insert** allows the user to insert an element into each data structure. 

The spinbox **Remove** allows the user to delete an element from each data structure. 

The spinbox **Find** allows the user to find an element from each data structure.

### Skip List Animation Overview


### Fibonacci Heap Animation Overview
Once elements are inserted, the minimum element is placed at the beginning of the root list and colored light blue. The double arrows represent a circular doubly linked list. 

When inserting a new element, the algorithm checks if it is less than the existing minimum. If it is, the element is put at the beginning of the root list and colored light blue.

When deleting an element, the algorithm searches for the value. Nodes that have been searched are colored red. When the node is found, the animation removes the value and then calls merge. Each step of the merge function is shown in the animation.

When finding an element, the animation colors visited nodes pink. When it finds a root element of a tree that is less than the element it is searching for, it traverses the tree. If/when the element is found, it terminates.


### Red-Black Tree Animation Overview


### Assignments:
* Skiplist: Scott, Sam
* Fib Heap: Abbie, Audrey
* RBT: Summer, Kevin
