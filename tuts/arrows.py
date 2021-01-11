from tkinter import *

root = Tk()
root.title('Codemy.com')
root.geometry("800x600")

w = 600
h = 400
x = w/2
y = h/2
x1 = 290
y1 = 190

my_canvas = Canvas(root, width=w, heigh=h, bg="white")
my_canvas.pack(pady=20)

my_circle = my_canvas.create_oval(x, y, x+20, y+20)
my_circle1 = my_canvas.create_oval(x1, y1, x1+20, y1+20, fill='red')

def left(event):
	x = -10
	y = 0
	x1 = -10
	y1 = 0
	my_canvas.move(my_circle, x, y)
	my_canvas.move(my_circle1, x1, y1)

def right(event):
	x = 10
	y = 0
	my_canvas.move(my_circle, x, y)


def up(event):
	x = 0
	y = -10
	my_canvas.move(my_circle, x, y)


def down(event):
	x = 0
	y = 10
	my_canvas.move(my_circle, x, y)

def pressing(event):
	x = 0
	y = 0
	if event.char == "a": x = -10
	if event.char == "d": x = 10
	if event.char == "r": y = -10
	if event.char == "x": y = 10
	my_canvas.move(my_circle, x, y)
	


root.bind("<Key>", pressing)


root.bind("<Left>", left)
root.bind("<Right>", right)
root.bind("<Up>", up)
root.bind("<Down>", down)




root.mainloop()

