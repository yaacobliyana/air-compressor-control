from tkinter import *
from tkinter import font
from PIL import ImageTk,Image
import sys
import time
import random
import calendar
import threading
import datetime as dt
import RPi.GPIO as GPIO

switch = True

root = Tk()
root.geometry("800x420")
root.title("LED TEST")
root.configure(bg='black')

led1 = 23
led2 = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led1,GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)

class Clock(Label):
    """ Class that contains the clock widget and clock refresh """

    def __init__(self, parent=None, seconds=True, colon=False):
        """
        Create and place the clock widget into the parent element
        It's an ordinary Label element with two additional features.
        """
        Label.__init__(self, parent)

        self.display_seconds = seconds
        if self.display_seconds:
            self.time     = time.strftime('%I:%M:%S %p')
        else:
            self.time     = time.strftime('%I:%M:%S %p').lstrip('0')
        self.display_time = self.time
        self.configure(text=self.display_time)

        if colon:
            self.blink_colon()

        self.after(200, self.tick)


    def tick(self):
        """ Updates the display clock every 200 milliseconds """
        if self.display_seconds:
            new_time = time.strftime('%I:%M:%S %p')
        else:
            new_time = time.strftime('%I:%M:%S %p').lstrip('0')
        if new_time != self.time:
            self.time = new_time
            self.display_time = self.time
            self.config(text=self.display_time)
        self.after(200, self.tick)


    def blink_colon(self):
        """ Blink the colon every second """
        if ':' in self.display_time:
            self.display_time = self.display_time.replace(':',' ')
        else:
            self.display_time = self.display_time.replace(' ',':',1)
        self.config(text=self.display_time)
        self.after(1000, self.blink_colon)
        
        
class timer(Label):
    def __init__(self):
        Tk.__init__(self)
        self.label = Label(self, text="", width=10)
        self.label.pack()
        self.remaining = 0
        self.countdown(10)

    def countdown(self, remaining = None):
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.label.configure(text="time's up!")
        else:
            self.label.configure(text="%d" % self.remaining)
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)
            
        
def startSystem():
    def run():
        while (switch == True):                
            GPIO.output(led1, True)
            GPIO.output(led2, False)
            time.sleep(5)
            GPIO.output(led1, False)
            GPIO.output(led2, True)
            time.sleep(5)
            if switch == False:
                break
            
    thread = threading.Thread(target=run)
    thread.start()

def switchon():
    global switch
    switch = True
    print('System is running')
    startSystem()
    
def switchoff():
    print('System exited')
    global switch
    switch = False
    GPIO.output(led1, False)
    GPIO.output(led2, False)
    
def on_led1():
    GPIO.output(led1, True)

def off_led1():
    GPIO.output(led1, False)

def on_led2():
    GPIO.output(led2, True)

def off_led2():
    GPIO.output(led2, False)
        
#Toggle Switch for Compressor 1
def toggle1():
    if led1_btn.config('text')[-1] == 'ON':
        led1_btn.config(text='OFF',width=4, height=2,
                     bg="#D9290B", fg="black",
                     font=('URW Gothic L', 16, 'bold'),
                     activebackground='#AE220B')
        print ("pressed true")
        on_led1()
    else:
        led1_btn.config(text='ON', width=4, height=2,
                     bg="#4EA20E", fg="black",
                     font=('URW Gothic L', 16, 'bold'),
                     activebackground='#428C09',)
        off_led1()


#Toggle Switch for Compressor 2
def toggle2():
    if led2_btn.config('text')[-1] == 'ON':
        led2_btn.config(text='OFF',width=4, height=2,
                     bg="#D9290B", fg="black",
                     font=('URW Gothic L', 16, 'bold'),
                     activebackground='#AE220B')
        print ("pressed true")
        on_led2()
    else:
        led2_btn.config(text='ON', width=4, height=2,
                     bg="#4EA20E", fg="black",
                     font=('URW Gothic L', 16, 'bold'),
                     activebackground='#428C09',)
        off_led2()
        
        
#########################################################
#                                                       #
#                    ADDING WIDGETS                     #
#                                                       #
#########################################################
#
#Inserting Elquator Logo
logo = Image.open('elquator.png')
resizedlogo = logo.resize((120, 120), Image.ANTIALIAS)
newlogo = ImageTk.PhotoImage(resizedlogo)
elquator = Label(root, image=newlogo)

#Inserting title
title = Label(root, text='AIR COMPRESSOR CONTROL SYSTEM',
              font=('Quicksand', 24),
              bg='black', fg='white')

#Inserting clock
clock1 = Clock(root)
clock1.configure(bg='black',fg='white',font=("helvetica",16, 'bold'))
#Adding date
date = Label(root, text=f"{dt.datetime.now():%a, %b %d %Y}",
             fg="white", bg="black", font=("helvetica",14))

#Inserting timer
timer1 = timer(root)
timer1.configure(bg='black',fg='white',font=("helvetica",16, 'bold'))


#START Button
start_btn = Button(root, text="START", width=8, height=2,
               bg="#4EA20E", fg="black",
               font=('URW Gothic L', 16, 'bold'),
               activebackground='#428C09', command=switchon)

stop_btn = Button(root, text='STOP',width=8, height=2,
                  bg="#D9290B", fg="black",
                  font=('URW Gothic L', 16, 'bold'),
                  activebackground='#AE220B', command=switchoff)

#Frame for LED1 button
frame1 = LabelFrame(root, text='Compressor 1', padx=15, pady=15,
                   font=('Quicksand',14), bg='black', fg='white')

#ON_LED1 Toggle Button
led1_btn = Button(frame1, text="ON", width=4, height=2,
               bg="#4EA20E", fg="black",
               font=('URW Gothic L', 16, 'bold'),
               activebackground='#428C09', command=toggle1)

#Frame for LED1 button
frame2 = LabelFrame(root, text='Compressor 1', padx=15, pady=15,
                   font=('Quicksand',14), bg='black', fg='white')

#ON_LED2 Toggle Button
led2_btn = Button(frame2, text="ON", width=4, height=2,
               bg="#4EA20E", fg="black",
               font=('URW Gothic L', 16, 'bold'),
               activebackground='#428C09', command=toggle2)



exit_btn = Button(root, text="Quit", width=4, height=1,
                  bg="black", fg="white",
                  command=lambda root=root:quit(root))


##DISPLAYING VARIABLE ON SCREEN
#
title.place(x=190,y=25)
#frame.pack(padx=10, pady=10)
elquator.place(x=40,y=35)
start_btn.place(x=40,y=200)
stop_btn.place(x=40,y=300)
frame1.place(x=640,y=80)
led1_btn.pack()
frame2.place(x=640,y=220)
led2_btn.pack()

date.place(x=260,y=70)
clock1.place(x=410,y=67)
timer1.place(x=260,y=170)

exit_btn.place(x=730,y=380)

root.mainloop()
