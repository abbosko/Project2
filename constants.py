from tkinter import * 

nodeColor = "yellow"
insertColor = "blue"
removeColor = "red"
findColor = "magenta"

# Global variables
canvasWidth = 800
canvasHeight = 400
padX = 50
padY = 50
spinboxWidth = 5

def calculateRadius(key):
    if(10 + (len(str(key))) * 1.2 > 12.4):
        return 10 + (len(str(key))) * 1.2   # determine radius of node based on length of the string
    else:
        return 12.4
    
def getCanvasX(canvas: Canvas):
    return canvas.winfo_width()

def getCanvasY(canvas: Canvas):
    return canvas.winfo_height()
