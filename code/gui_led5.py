from tkinter import *
import RPi.GPIO as GPIO
import time
import threading
from random import randint


switch = True
remaining = 0

root = Tk()
root.geometry("600x600")
root.title("LED TEST")

led1 = 23
led2 = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led1,GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)

def startSystem():
    def run():
        while (switch == True):                
            GPIO.output(led1, True)
            GPIO.output(led2, False)
            time.sleep(1)
            GPIO.output(led1, False)
            GPIO.output(led2, True)
            time.sleep(1)
            if switch == False:
                break
            
    thread = threading.Thread(target=run)
    thread.start()
    
def countdown():
    remaining = 10

    if remaining <= 0:
        timer.config(text="time's up!")
    else:
        root.after(1000, countdown)
        remaining = remaining - 1  
        timer.config(text="%d" % remaining)

def switchon():
    global switch
    switch = True
    print('System is running')
    startSystem()
    countdown()
    
def switchoff():
    print('System exited')
    global switch
    switch = False
    GPIO.output(led1, False)
    GPIO.output(led2, False)
    
def kill():
    root.destroy()

def rando():
    random_label.config(text=f'Random Number: {randint(1,100)}')

def on_led1():
    GPIO.output(led1, True)

def off_led1():
    GPIO.output(led1, False)

def on_led2():
    GPIO.output(led2, True)

def off_led2():
    GPIO.output(led2, False)
    

B1 = Button(root, text="ON", width=20, bg="green", fg="black", command=on_led1)
B1.place(x=150,y=50)

B2 = Button(root, text="OFF", width=20, bg="red", fg="black", command=off_led1)
B2.place(x=350,y=50)

B3 = Button(root, text="ON", width=20, bg="green", fg="black", command=on_led2)
B3.place(x=150,y=100)

B4 = Button(root, text="OFF", width=20, bg="red", fg="black", command=off_led2)
B4.place(x=350,y=100)

B5 = Button(root, text="START", width=20, bg="yellow", fg="black", command=switchon)
B5.place(x=150,y=150)
timer = Label(root)
timer.pack(pady=20)

B6 = Button(root, text="STOP", width=20, bg="red", fg="black", command=switchoff)
B6.place(x=350,y=150)

my_button2 = Button(root, text="Pick Random Number", command=rando)
my_button2.pack(pady=200)

random_label = Label(root, text='')
random_label.pack(padx=20,pady=20)

killbutton = Button(root, text = "EXIT", command = kill)    
killbutton.pack(padx=10)   

#threading.Thread(target=startSystem).start()

root.mainloop()

