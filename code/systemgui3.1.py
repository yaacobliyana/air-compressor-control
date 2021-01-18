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

#Importing MCP libraries
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
#defining MCP
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D22)
mcp = MCP.MCP3008(spi, cs)
chan0 = AnalogIn(mcp, MCP.P0)
chan1 = AnalogIn(mcp, MCP.P1)


switch = True

root = Tk()
root.geometry("800x420")
root.title("LED TEST")

#Placing a background image
bg = Image.open('spacepi.png')
bgg = ImageTk.PhotoImage(bg)
labelbg = Label(root, image=bgg)
labelbg.place(x=0, y=0, relwidth=1, relheight=1)

#Defining LEDs setup
led1 = 23
led2 = 24
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led1,GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)

#Class for displaying time and date
#
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


#Spawning Message box for Warning
#
def choice(option):
    pop.destroy()

    if option == "yes":
        print("You Clicked Yes!")
        switchon()
    else:
        print("You Clicked No!!")

def messagebox():

    global pop
    pop = Toplevel(root)
    pop.title("Warning Message")
    pop.config(bg='white')
    pop.geometry("250x120")

    global warn
    warn = PhotoImage(file="warning.png")

    pop_label1 = Label(pop, text="You are about to start the system.", 
                        font=("URW Gothic L", 12))
    pop_label1.pack(pady=5)

    pop_label1 = Label(pop, text="Would you like to proceed?", 
                        font=("URW Gothic L", 12))
    pop_label1.pack(pady=3)

    my_frame = Frame(pop, bg='white')
    my_frame.pack(pady=3)

    me_pic = Label(my_frame, image=warn, borderwidth=0)
    me_pic.grid(row=0, column=0, padx=5)

    yes = Button(my_frame, text="YES", command=lambda: choice("yes"), bg="orange")
    yes.grid(row=0, column=1, padx=5)

    no = Button(my_frame, text="NO", command=lambda: choice("no"), bg="yellow")
    no.grid(row=0, column=2, padx=5)

def mcp_update():
    global v1
    global v2
    v1 = chan0.voltage
    v2 = chan1.voltage
    print('ADC Voltage 1: ' + str(chan0.voltage) + 'V')
    print('ADC Voltage 2: ' + str(chan1.voltage) + 'V')

#Start System function
def switchon():
    global switch
    mcp_update()
    if (v1 > 3.0 and v2 > 3.0):
        time.sleep(5)
        switch = True
        print('System is running')
        step()
        anic1()
    else:
        switch == False
        switchoff()

#Turning off system function
def switchoff():
    print('System exited')
    global switch
    switch = False
    GPIO.output(led1, False)
    GPIO.output(led2, False)
    #bstop()
    circlez()
    
def blink_path1():
    start = time.time()
    i = 10
    while i > 0:
        if (v1 > 3.0 and v2 > 3.0):
            i = 11 - (time.time() - start)
            tlabel.config(text=str(int(i))+" secs")
            GPIO.output(led1, True)
            GPIO.output(led2, False)
            mcp_update()
            circlez_1a()
            time.sleep(0.1)
            circlez_1b()
            time.sleep(0.1)
        else:
            switch == False
            switchoff()
        if switch == False:
                break 
 

def blink_path2():
    start = time.time()
    i = 10
    while i > 0:
        if (v1 > 3.0 and v2 > 3.0):
            i = 11 - (time.time() - start)
            tlabel1.config(text=str(int(i))+" secs")
            GPIO.output(led2, True)
            GPIO.output(led1, False)
            mcp_update()
            circlez_2a()
            time.sleep(0.1)
            circlez_2b()
            time.sleep(0.1)
        else:
            switch == False
            switchoff()
        if switch == False:
                break

def anic1():
    def run_anic1():
        full=5
        i=0
        while (i<full):
            i += 1
            blink_path1()
            blink_path2()
            if (i==full or switch == False):
                if not switchoff():
                    break
    tra = threading.Thread(target=run_anic1)
    tra.start()

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
        led1_btn.config(text='OFF', image=offb, bg='black', borderwidth=0)
        print ("pressed true")
        on_led1()
    else:
        led1_btn.config(text='ON', image=onb, bg='black', borderwidth=0)
        off_led1()


#Toggle Switch for Compressor 2
def toggle2():
    if led2_btn.config('text')[-1] == 'ON':
        led2_btn.config(text='OFF', image=offb, bg='black', borderwidth=0)
        print ("pressed true")
        on_led2()
    else:
        led2_btn.config(text='ON', image=onb, bg='black', borderwidth=0)
        off_led2()
        
def step():
    def runn():
        full = 100
        i = 0
        while(i<full):
            time.sleep(1)
            pbar['value']+=1
            i+=1
            percent.set(str(int((i/full)*100))+"%")
            root.update_idletasks()
            if (i == full or switch == False):
                break
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
    c2 = dance.create_oval(145,75,155,85,fill='blue')
    c3 = dance.create_oval(160,75,170,85,fill='white')
    c4 = dance.create_oval(175,75,185,85,fill='blue')
    c5 = dance.create_oval(190,75,200,85,fill='white')
    c6 = dance.create_oval(205,75,215,85,fill='blue')
    c7 = dance.create_oval(220,75,230,85,fill='white')
    c8 = dance.create_oval(220,60,230,70,fill='blue')
    c9 = dance.create_oval(220,45,230,55,fill='white')
    c10 = dance.create_oval(235,45,245,55,fill='blue')
    c11 = dance.create_oval(250,45,260,55,fill='white')
    c12 = dance.create_oval(265,45,275,55,fill='blue')
    c13 = dance.create_oval(280,45,290,55,fill='white')
    c14 = dance.create_oval(295,45,305,55,fill='blue')
    c15 = dance.create_oval(310,45,320,55,fill='white')
    c16 = dance.create_oval(325,45,335,55,fill='blue')
    
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
    c1 = dance.create_oval(130,75,140,85,fill='blue')
    c2 = dance.create_oval(145,75,155,85,fill='white')
    c3 = dance.create_oval(160,75,170,85,fill='blue')
    c4 = dance.create_oval(175,75,185,85,fill='white')
    c5 = dance.create_oval(190,75,200,85,fill='blue')
    c6 = dance.create_oval(205,75,215,85,fill='white')
    c7 = dance.create_oval(220,75,230,85,fill='blue')
    c8 = dance.create_oval(220,60,230,70,fill='white')
    c9 = dance.create_oval(220,45,230,55,fill='blue')
    c10 = dance.create_oval(235,45,245,55,fill='white')
    c11 = dance.create_oval(250,45,260,55,fill='blue')
    c12 = dance.create_oval(265,45,275,55,fill='white')
    c13 = dance.create_oval(280,45,290,55,fill='blue')
    c14 = dance.create_oval(295,45,305,55,fill='white')
    c15 = dance.create_oval(310,45,320,55,fill='blue')
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
    
def circlez_2a():
    c1 = dance.create_oval(130,75,140,85,fill='white')
    c2 = dance.create_oval(145,75,155,85,fill='white')
    c3 = dance.create_oval(160,75,170,85,fill='white')
    c4 = dance.create_oval(175,75,185,85,fill='white')
    c5 = dance.create_oval(190,75,200,85,fill='white')
    c6 = dance.create_oval(205,75,215,85,fill='white')

    c17 = dance.create_oval(130,210,140,220,fill='white')
    c18 = dance.create_oval(145,210,155,220,fill='magenta')
    c19 = dance.create_oval(160,210,170,220,fill='white')
    c20 = dance.create_oval(175,210,185,220,fill='magenta')
    c21 = dance.create_oval(190,210,200,220,fill='white')
    c22 = dance.create_oval(205,210,215,220,fill='magenta')
    c23 = dance.create_oval(220,210,230,220,fill='white')
    c24 = dance.create_oval(220,195,230,205,fill='magenta')
    c25 = dance.create_oval(220,180,230,190,fill='white')
    c26 = dance.create_oval(220,165,230,175,fill='magenta')
    c27 = dance.create_oval(220,150,230,160,fill='white')
    c28 = dance.create_oval(220,135,230,145,fill='magenta')
    c29 = dance.create_oval(220,120,230,130,fill='white')
    c30 = dance.create_oval(220,105,230,115,fill='magenta')
    c31 = dance.create_oval(220,90,230,100,fill='white')
    c7 = dance.create_oval(220,75,230,85,fill='magenta')
    c8 = dance.create_oval(220,60,230,70,fill='white')
    c9 = dance.create_oval(220,45,230,55,fill='magenta')
    c10 = dance.create_oval(235,45,245,55,fill='white')
    c11 = dance.create_oval(250,45,260,55,fill='magenta')
    c12 = dance.create_oval(265,45,275,55,fill='white')
    c13 = dance.create_oval(280,45,290,55,fill='magenta')
    c14 = dance.create_oval(295,45,305,55,fill='white')
    c15 = dance.create_oval(310,45,320,55,fill='magenta')
    c16 = dance.create_oval(325,45,335,55,fill='white')
    
def circlez_2b():
    c1 = dance.create_oval(130,75,140,85,fill='white')
    c2 = dance.create_oval(145,75,155,85,fill='white')
    c3 = dance.create_oval(160,75,170,85,fill='white')
    c4 = dance.create_oval(175,75,185,85,fill='white')
    c5 = dance.create_oval(190,75,200,85,fill='white')
    c6 = dance.create_oval(205,75,215,85,fill='white')

    c17 = dance.create_oval(130,210,140,220,fill='magenta')
    c18 = dance.create_oval(145,210,155,220,fill='white')
    c19 = dance.create_oval(160,210,170,220,fill='magenta')
    c20 = dance.create_oval(175,210,185,220,fill='white')
    c21 = dance.create_oval(190,210,200,220,fill='magenta')
    c22 = dance.create_oval(205,210,215,220,fill='white')
    c23 = dance.create_oval(220,210,230,220,fill='magenta')
    c24 = dance.create_oval(220,195,230,205,fill='white')
    c25 = dance.create_oval(220,180,230,190,fill='magenta')
    c26 = dance.create_oval(220,165,230,175,fill='white')
    c27 = dance.create_oval(220,150,230,160,fill='magenta')
    c28 = dance.create_oval(220,135,230,145,fill='white')
    c29 = dance.create_oval(220,120,230,130,fill='magenta')
    c30 = dance.create_oval(220,105,230,115,fill='white')
    c31 = dance.create_oval(220,90,230,100,fill='magenta')
    c7 = dance.create_oval(220,75,230,85,fill='white')
    c8 = dance.create_oval(220,60,230,70,fill='magenta')
    c9 = dance.create_oval(220,45,230,55,fill='white')
    c10 = dance.create_oval(235,45,245,55,fill='magenta')
    c11 = dance.create_oval(250,45,260,55,fill='white')
    c12 = dance.create_oval(265,45,275,55,fill='magenta')
    c13 = dance.create_oval(280,45,290,55,fill='white')
    c14 = dance.create_oval(295,45,305,55,fill='magenta')
    c15 = dance.create_oval(310,45,320,55,fill='white')
    c16 = dance.create_oval(325,45,335,55,fill='magenta')
            
    

#########################################################
#                                                       #
#                    ADDING WIDGETS                     #
#                                                       #
#########################################################
#
#Inserting frame for animation
dance = Canvas(root, bg='black',width=425,height=265)
#Draw many many circles (put in a function)
circlez()

#Inserting Elquator Logo
logo = Image.open('elquator.png')
resizedlogo = logo.resize((120, 120), Image.ANTIALIAS)
newlogo = ImageTk.PhotoImage(resizedlogo)
elquator = Label(root, image=newlogo)

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

#Inserting Start Button Image
sb = Image.open('start.png')
res_sb = sb.resize((167, 70), Image.ANTIALIAS)
newsb = ImageTk.PhotoImage(res_sb)

#Inserting Stop Button Image
stopb = Image.open('stop.png')
res_stopb = stopb.resize((167, 70), Image.ANTIALIAS)
newstopb = ImageTk.PhotoImage(res_stopb)

#Inserting ON Button Image
on = Image.open('on.png')
res_on = on.resize((80, 80), Image.ANTIALIAS)
onb = ImageTk.PhotoImage(res_on)

#Inserting OFF Button Image
off = Image.open('off.png')
res_off = off.resize((80, 80), Image.ANTIALIAS)
offb = ImageTk.PhotoImage(res_off)


#Inserting clock
clock1 = Clock(root)
clock1.configure(bg='black',fg='white',font=("helvetica",16, 'bold'))
#Adding date
date = Label(root, text=f"{dt.datetime.now():%a, %b %d %Y}",
             fg="white", bg="black", font=("helvetica",14))

#START Button
start_btn = Button(root, image=newsb, command=messagebox, 
                    borderwidth=0, bg='black')
#STOP Button
stop_btn = Button(root, image=newstopb, command=switchoff,
                    borderwidth=0, bg='black')

#ON_LED1 Toggle Button
led1_btn = Button(root, text='ON', image=onb, command=toggle1,
                    borderwidth=0, bg='black')

#ON_LED2 Toggle Button
led2_btn = Button(root, text='ON', image=onb, command=toggle2,
                    borderwidth=0, bg='black')

#Inserting progress bar
percent = StringVar()
pbar = ttk.Progressbar(root, orient=VERTICAL,
                       length = 220,mode='determinate')
#Inserting progress bar label
plabel = Label(root, textvariable=percent, font=('Quicksand',10),
                bg='black', fg='white')

#Inserting timer1 label
tlabel = Label(root, text=' ', font=('Quicksand', 14),
                bg='black', fg='white')

#Inserting timer2 label
tlabel1 = Label(root, text=' ', font=('Quicksand', 14),
                bg='black', fg='white' )

#Inserting compressor 1 label
clabel1 = Label(root, text='C1', font=('URW Gothic L', 14, 'bold'),
          bg='black', fg='white' )

#Inserting compressor 2 label
clabel2 = Label(root, text='C2', font=('URW Gothic L', 14, 'bold'),
          bg='black', fg='white' )


#Inserting exit button
exit_btn = Button(root, text="Quit", width=4, height=1,
                  bg="black", fg="white",
                  command=lambda root=root:quit(root))


##DISPLAYING VARIABLE ON SCREEN
#
elquator.place(x=30,y=35)
date.place(x=260,y=70)
clock1.place(x=410,y=67)

start_btn.place(x=15,y=250)
stop_btn.place(x=15,y=330)
led1_btn.place(x=680,y=140)
led2_btn.place(x=680,y=280)

dance.place(x=205,y=120)
plabel.place(x=585,y=130)
pbar.place(x=595,y=155)
tank.place(x=525,y=155)
airComp.place(x=220,y=140)
clabel1.place(x=267,y=187) 
tlabel.place(x=330,y=210)
airComp1.place(x=220,y=275)
clabel2.place(x=267,y=322) 
tlabel1.place(x=330,y=340) 

exit_btn.place(x=730,y=380)

root.mainloop()
