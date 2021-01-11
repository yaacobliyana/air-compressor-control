from tkinter import *
from tkinter import ttk
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
        
def startSystem():
    def run():
        while (switch == True):                
            GPIO.output(led1, True)
            GPIO.output(led2, False)
            time.sleep(3)
            GPIO.output(led1, False)
            GPIO.output(led2, True)
            time.sleep(3)
            if switch == False:
                break
            
    thread = threading.Thread(target=run)
    thread.start()
'''    
def countdown():
    def runn():
        rem = 0
        for (i)
'''
def switchon():
    global switch
    switch = True
    print('System is running')
    startSystem()
    step()
    
def switchoff():
    print('System exited')
    global switch
    switch = False
    GPIO.output(led1, False)
    GPIO.output(led2, False)
    bstop()
    
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
        
def step():
    def runn():
        full = 10
        i = 0
        while(i<full):
            time.sleep(1)
            pbar['value']+=10
            i+=1
            percent.set(str(int((i/full)*100))+"%")
            root.update_idletasks()
            if i==full:
                switchoff()
            
    ts = threading.Thread(target=runn)
    ts.start()
    
def bstop():
    pbar.stop()
    
def circlez():
    c1 = dance.create_oval(130,75,140,85,fill='white')
    c2 = dance.create_oval(145,75,155,85,fill='white')
    c3 = dance.create_oval(160,75,170,85,fill='white')
    c4 = dance.create_oval(175,75,185,85,fill='white')
    c5 = dance.create_oval(190,75,200,85,fill='white')
    c6 = dance.create_oval(205,75,215,85,fill='white')
    c7 = dance.create_oval(220,75,230,85,fill='white')
    c8 = dance.create_oval(220,60,230,70,fill='white')
    c9 = dance.create_oval(220,45,230,55,fill='white')
    c10 = dance.create_oval(235,45,245,55,fill='white')
    c11 = dance.create_oval(250,45,260,55,fill='white')
    c12 = dance.create_oval(265,45,275,55,fill='white')
    c13 = dance.create_oval(280,45,290,55,fill='white')
    c14 = dance.create_oval(295,45,305,55,fill='white')
    c15 = dance.create_oval(310,45,320,55,fill='white')
    c16 = dance.create_oval(325,45,335,55,fill='white')
    
    c17 = dance.create_oval(130,210,140,220,fill='white')
    c18 = dance.create_oval(145,210,155,220,fill='white')
    c19 = dance.create_oval(160,210,170,220,fill='white')
    c20 = dance.create_oval(175,210,185,220,fill='white')
    c21 = dance.create_oval(190,210,200,220,fill='white')
    c22 = dance.create_oval(205,210,215,220,fill='white')
    c23 = dance.create_oval(220,210,230,220,fill='white')
    c24 = dance.create_oval(220,195,230,205,fill='white')
    c25 = dance.create_oval(220,180,230,190,fill='white')
    c26 = dance.create_oval(220,165,230,175,fill='white')
    c27 = dance.create_oval(220,150,230,160,fill='white')
    c28 = dance.create_oval(220,135,230,145,fill='white')
    c29 = dance.create_oval(220,120,230,130,fill='white')
    c30 = dance.create_oval(220,105,230,115,fill='white')
    c31 = dance.create_oval(220,90,230,100,fill='white')
    
def circlez_1a():
    c1 = dance.create_oval(130,75,140,85,fill='white')
    c2 = dance.create_oval(145,75,155,85,fill='cyan')
    c3 = dance.create_oval(160,75,170,85,fill='white')
    c4 = dance.create_oval(175,75,185,85,fill='cyan')
    c5 = dance.create_oval(190,75,200,85,fill='white')
    c6 = dance.create_oval(205,75,215,85,fill='cyan')
    c7 = dance.create_oval(220,75,230,85,fill='white')
    c8 = dance.create_oval(220,60,230,70,fill='cyan')
    c9 = dance.create_oval(220,45,230,55,fill='white')
    c10 = dance.create_oval(235,45,245,55,fill='cyan')
    c11 = dance.create_oval(250,45,260,55,fill='white')
    c12 = dance.create_oval(265,45,275,55,fill='cyan')
    c13 = dance.create_oval(280,45,290,55,fill='white')
    c14 = dance.create_oval(295,45,305,55,fill='cyan')
    c15 = dance.create_oval(310,45,320,55,fill='white')
    c16 = dance.create_oval(325,45,335,55,fill='cyan')
    
    c17 = dance.create_oval(130,210,140,220,fill='white')
    c18 = dance.create_oval(145,210,155,220,fill='white')
    c19 = dance.create_oval(160,210,170,220,fill='white')
    c20 = dance.create_oval(175,210,185,220,fill='white')
    c21 = dance.create_oval(190,210,200,220,fill='white')
    c22 = dance.create_oval(205,210,215,220,fill='white')
    c23 = dance.create_oval(220,210,230,220,fill='white')
    c24 = dance.create_oval(220,195,230,205,fill='white')
    c25 = dance.create_oval(220,180,230,190,fill='white')
    c26 = dance.create_oval(220,165,230,175,fill='white')
    c27 = dance.create_oval(220,150,230,160,fill='white')
    c28 = dance.create_oval(220,135,230,145,fill='white')
    c29 = dance.create_oval(220,120,230,130,fill='white')
    c30 = dance.create_oval(220,105,230,115,fill='white')
    c31 = dance.create_oval(220,90,230,100,fill='white')

def circlez_1b():
    c1 = dance.create_oval(130,75,140,85,fill='cyan')
    c2 = dance.create_oval(145,75,155,85,fill='white')
    c3 = dance.create_oval(160,75,170,85,fill='cyan')
    c4 = dance.create_oval(175,75,185,85,fill='white')
    c5 = dance.create_oval(190,75,200,85,fill='cyan')
    c6 = dance.create_oval(205,75,215,85,fill='white')
    c7 = dance.create_oval(220,75,230,85,fill='cyan')
    c8 = dance.create_oval(220,60,230,70,fill='white')
    c9 = dance.create_oval(220,45,230,55,fill='cyan')
    c10 = dance.create_oval(235,45,245,55,fill='white')
    c11 = dance.create_oval(250,45,260,55,fill='cyan')
    c12 = dance.create_oval(265,45,275,55,fill='white')
    c13 = dance.create_oval(280,45,290,55,fill='cyan')
    c14 = dance.create_oval(295,45,305,55,fill='white')
    c15 = dance.create_oval(310,45,320,55,fill='cyan')
    c16 = dance.create_oval(325,45,335,55,fill='white')
    
    c17 = dance.create_oval(130,210,140,220,fill='white')
    c18 = dance.create_oval(145,210,155,220,fill='white')
    c19 = dance.create_oval(160,210,170,220,fill='white')
    c20 = dance.create_oval(175,210,185,220,fill='white')
    c21 = dance.create_oval(190,210,200,220,fill='white')
    c22 = dance.create_oval(205,210,215,220,fill='white')
    c23 = dance.create_oval(220,210,230,220,fill='white')
    c24 = dance.create_oval(220,195,230,205,fill='white')
    c25 = dance.create_oval(220,180,230,190,fill='white')
    c26 = dance.create_oval(220,165,230,175,fill='white')
    c27 = dance.create_oval(220,150,230,160,fill='white')
    c28 = dance.create_oval(220,135,230,145,fill='white')
    c29 = dance.create_oval(220,120,230,130,fill='white')
    c30 = dance.create_oval(220,105,230,115,fill='white')
    c31 = dance.create_oval(220,90,230,100,fill='white')
    
def anic1():
    def run_anic1:
        while (switch == True):
            circlez_1a()
            time.sleep(1)
            circlez_1b
            time.sleep(1)
            if switch == False:
                break
            
    

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

#Inserting frame for animation
dance = Canvas(root, bg='black',width=425,height=265)
#Draw many many circles (put in a function)
circlez()

#Inserting Compressor Icon
ac = Image.open('airComp.png')
res_ac = ac.resize((105, 100), Image.ANTIALIAS)
newac = ImageTk.PhotoImage(res_ac)
airComp = Label(root, image=newac, bg='black')

#Inserting second Compressor Icon
ac1 = Image.open('airComp.png')
res_ac1 = ac1.resize((105, 100), Image.ANTIALIAS)
newac1 = ImageTk.PhotoImage(res_ac1)
airComp1 = Label(root, image=newac1, bg='black')

#Inserting Tank Icon
gt = Image.open('tank.png')
res_gt = gt.resize((54, 220), Image.ANTIALIAS)
newgt = ImageTk.PhotoImage(res_gt)
tank = Label(root, image=newgt, bg='black')

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

#Inserting progress bar
percent = StringVar()
pbar = ttk.Progressbar(root, orient=VERTICAL,
                       length = 220,mode='determinate')
#Inserting progress bar label
plabel = Label(root, textvariable=percent, font=('Quicksand',10),
                bg='black', fg='white')


#Inserting exit button
exit_btn = Button(root, text="Quit", width=4, height=1,
                  bg="black", fg="white",
                  command=lambda root=root:quit(root))


##DISPLAYING VARIABLE ON SCREEN
#
title.place(x=190,y=25)
elquator.place(x=40,y=35)
date.place(x=260,y=70)
clock1.place(x=410,y=67)

start_btn.place(x=40,y=200)
stop_btn.place(x=40,y=300)
frame1.place(x=650,y=80)
led1_btn.pack()
frame2.place(x=650,y=220)
led2_btn.pack()

dance.place(x=200,y=120)
plabel.place(x=585,y=130)
pbar.place(x=590,y=155)
tank.place(x=520,y=155)
airComp.place(x=220,y=140)
airComp1.place(x=220,y=275)

exit_btn.place(x=730,y=380)

root.mainloop()
