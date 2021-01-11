import time
from tkinter import *

root = Tk()
root.geometry("100x100")


def update():
    print (number)

for number in range(10,0,-1):
    update()
    
l = Label(root, text=' ')
l.pack()
l.after(10000, update)