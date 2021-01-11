from tkinter import *
import RPi.GPIO as GPIO
import time
import threading
from random import randint


switch = True

root = Tk()
root.geometry("600x600")
root.title("LED TEST")

led1 = 23
led2 = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led1,GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)


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
    
def toggle1():
    '''
    use
    t_btn.config('text')[-1]
    to get the present state of the toggle button
    '''
    if t_btn.config('text')[-1] == 'ON':
        t_btn.config(text='OFF',width=8, height=2,
                     bg="#D9290B", fg="black",
                     font=('URW Gothic L', 16, 'bold'),
                     activebackground='#AE220B')
        print ("pressed true")
        on_led1()
    else:
        t_btn.config(text='ON', width=8, height=2,
                     bg="#4EA20E", fg="black",
                     font=('URW Gothic L', 16, 'bold'),
                     activebackground='#428C09',)
        off_led1()

t_btn = Button(root, text="ON", width=8, height=2,
               bg="#4EA20E", fg="black",
               font=('URW Gothic L', 16, 'bold'),
               activebackground='#428C09', command=toggle1)
t_btn.place(x=220,y=100)
