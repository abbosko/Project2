
from tkinter import *
import random
import time
import math
import sys

# maxDegree = int(input("Max degree of tree: "))
maxDegree = 5
tree = []
q = 0
for index, i in enumerate(range(maxDegree)):
    blank = []
    tree.append(blank)
    for j in range(int(math.pow(2, index))):
        tree[i].append(q)
        q += 1

root = Tk()
root.title("Data Structures Visualization")
root.maxsize(1920, 1080)
root.config(bg = "white")
random.seed(time.time())
# Global variables
canvasWidth = 800
canvasHeight = 400
padX = 50
padY = 50

# Calculates a radius such that the text within will fit into the circle
def calculateRadius(key):
    if(10 + (len(str(key))) * 1.2 > 12.4):
        return 10 + (len(str(key))) * 1.2   # determine radius of node based on length of the string
    else:
        return 12.4

def getCanvasX(canvas: Canvas):
    return canvasWidth

def getCanvasY(canvas: Canvas):
    return canvasHeight

# Calculates an X value
def findX(degree, rowIndex):
    global canvas
    return padX + (((getCanvasX(canvas) - (padX * 2)) / (math.pow(2, degree) + 1)) * (rowIndex + 1))

# Calculates a Y value
def findY(currDegree):
    global canvas
    return (((getCanvasY(canvas) + (padY * 2)) / ((len(tree)) + 1)) * (currDegree + 1)) - padY

# canvas
canvas = Canvas(root, width=canvasWidth, height=canvasHeight, bg="gray")
canvas.grid(row=0, column=0, padx=10, pady=5)

for degree, row in enumerate(tree):
    for rowIndex, element in enumerate(row):
        currX = findX(degree, rowIndex)
        currY = findY(degree)
        radius = calculateRadius(element)
        canvas.create_oval(currX-radius, currY-radius, currX+radius, currY+radius, fill="yellow")
        canvas.create_text(currX, currY, text=str(element), fill="black")

root.mainloop()
