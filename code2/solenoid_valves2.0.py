from tkinter import *
from PIL import ImageTk,Image
import sys
import time
import calendar
import gaugelib
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

#Defining and setting up relay pins
relay_pins = [13, 19, 26, 16, 20, 21]
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pins, GPIO.OUT)

switch = True
p1_value = 0
p2_value = 0

root = Tk()
root.geometry("800x420")
root.title("AIR COMPRESSOR CONTROL SYSTEM")
root.configure(bg='black')

#Read Pressure Sensor 1
def read_gauge():
    global switch
    global p1_value
    #time.sleep(0.1)
    v1 = chan0.voltage
    p1_value = (78*(v1-0.4787))
    p1.set_value(int(p1_value))
    print('ADC Voltage 1: ' + str(chan0.voltage) + 'V')
    print('Pressure: ' + str(int(p1_value)) + 'bar')
    root.update_idletasks()
    #root.after(100,read_gauge)


#Read Pressure Sensor 2
def read_gauge2():
    global switch
    global p2_value
    #time.sleep(0.1)
    v2 = chan1.voltage
    p2_value = (78*(v1-0.4787))
    p2.set_value(int(p2_value))
    print('ADC Voltage 1: ' + str(chan1.voltage) + 'V')
    print('Pressure: ' + str(int(p2_value)) + 'bar')
    root.update_idletasks()
    #root.after(100,read_gauge)

def closeAll():
    GPIO.output(13, True)
    GPIO.output(19, True)
    GPIO.output(26, True)
    GPIO.output(16, True)
    print('Close all valves')
    
#Start the Program for first sequence
def start1():
    read_gauge()
    if (p1_value <= 150) and (p1_value >= 50):
        read_gauge()
        GPIO.output(13, False)
        GPIO.output(19, False)
        GPIO.output(26, True)
        GPIO.output(16, True)
        print('open valve 1 & 2')
        print('close valve 3 & 4')
    if (p1_value < 50):
        closeAll()

#Start the Program for second sequence
def start2():
    read_gauge2()
    while (p2_value <= 150) and (p2_value >= 50):
        read_gauge2()
        GPIO.output(13, True)
        GPIO.output(19, True)
        GPIO.output(26, False)
        GPIO.output(16, False)
        print('open valve 3 & 4')
        print('close valve 1 & 2')
        if p2_value <= 50:
            if not closeAll():
                break
            
def arrow_path1():
    while switch == True:
        arroway11()
        arroway21()
        time.sleep(0.1)
        arroway12()
        arroway22()
        time.sleep(0.1)
        if switch == False:
            break      

def arrow_path1():
    while switch == True:
        arroway11()
        arroway21()
        time.sleep(0.1)
        arroway12()
        arroway22()
        time.sleep(0.1)
        if switch == False:
            break      


def start():
    def run():
        global switch
        switch = True
        while switch == True:
            start1()
            arrow_path1()
            #start2()
            if switch == False:
                break
    t = threading.Thread(target=run)
    t.start()
    
def stop():
    print('System exited')
    global switch
    switch = False
    closeAll()
    arroway10()
    arroway20()

####------ ADDING WIDGETS ------####

#Inserting frame for animation
path = Canvas(root, bg='black', width=600, height=300, 
                bd=0, highlightthickness=0, relief='ridge')

#Inserting Tank Image
gt = Image.open('images/tank.png')
res_gt = gt.resize((54, 220), Image.ANTIALIAS)
newgt = ImageTk.PhotoImage(res_gt)
tank = Label(root, image=newgt, bg='black')

#Inserting Tank 2 Image
gt2 = Image.open('images/tank2.png')
res_gt2 = gt2.resize((54, 220), Image.ANTIALIAS)
newgt2 = ImageTk.PhotoImage(res_gt2)
tank2 = Label(root, image=newgt2, bg='black')

#Inserting Turbine Image
tt = Image.open('images/turbine1.png')
res_tt = tt.resize((100, 100), Image.ANTIALIAS)
newtt = ImageTk.PhotoImage(res_tt)

#Inserting Turbine 2 Image
tt2 = Image.open('images/turbine3.png')
res_tt2 = tt2.resize((100, 100), Image.ANTIALIAS)
newtt2 = ImageTk.PhotoImage(res_tt2)

def placeTurbine1():
    global turbine
    turbine = Label(root, image=newtt, bg='black')
    turbine.place(x=350,y=137)
def placeTurbine2():
    global turbine
    turbine = Label(root, image=newtt2, bg='black')
    turbine.place(x=350,y=137)

placeTurbine1()

#Inserting Arrow Image
ar = Image.open('images/arrow.png')
res_ar = ar.resize((100, 27), Image.ANTIALIAS)
newar = ImageTk.PhotoImage(res_ar)

#Inserting Arrow Image
ar1 = Image.open('images/arrow1.png')
res_ar1 = ar1.resize((100, 27), Image.ANTIALIAS)
newar1 = ImageTk.PhotoImage(res_ar1)

#Inserting Arrow Image
ar2 = Image.open('images/arrow2.png')
res_ar2 = ar2.resize((100, 27), Image.ANTIALIAS)
newar2 = ImageTk.PhotoImage(res_ar2)

#Inserting Arrow Image
af = Image.open('images/arrowf.png')
res_af = af.resize((100, 27), Image.ANTIALIAS)
newaf = ImageTk.PhotoImage(res_af)

#Inserting Arrow Image
af1 = Image.open('images/arrowf1.png')
res_af1 = af1.resize((100, 27), Image.ANTIALIAS)
newaf1 = ImageTk.PhotoImage(res_af1)

#Inserting Arrow Image
af2 = Image.open('images/arrowf2.png')
res_af2 = af2.resize((100, 27), Image.ANTIALIAS)
newaf2 = ImageTk.PhotoImage(res_af2)

def arroway10():
    arrow = Label(root, image=newar, bg='black')
    arrow.place(x=245,y=140)

def arroway11():
    arrow1 = Label(root, image=newar1, bg='black')
    arrow1.place(x=245,y=140)

def arroway12():
    arrow2 = Label(root, image=newar2, bg='black')
    arrow2.place(x=245,y=140)   

def arroway20():
    arrow = Label(root, image=newar, bg='black')
    arrow.place(x=460,y=210)

def arroway21():
    arrow1 = Label(root, image=newar1, bg='black')
    arrow1.place(x=460,y=210)

def arroway22():
    arrow2 = Label(root, image=newar2, bg='black')
    arrow2.place(x=460,y=210)

def arroway30():
    arrow = Label(root, image=newaf, bg='black')
    arrow.place(x=460,y=140)

def arroway31():
    arrow1 = Label(root, image=newaf1, bg='black')
    arrow1.place(x=460,y=140)

def arroway32():
    arrow2 = Label(root, image=newaf2, bg='black')
    arrow2.place(x=460,y=140)

def arroway40():
    arrow = Label(root, image=newaf, bg='black')
    arrow.place(x=245,y=210)

def arroway41():
    arrow1 = Label(root, image=newaf1, bg='black')
    arrow1.place(x=245,y=210)

def arroway42():
    arrow2 = Label(root, image=newaf2, bg='black')
    arrow2.place(x=245,y=210)

arroway10()
arroway20()
arroway30()
arroway40()

#Inserting gauge widget
p1 = gaugelib.DrawGauge2(root, max_value=300.0, min_value=0.0,
                        size=140, bg_col='black',
                        unit="psi", bg_sel=2)
#Inserting gauge widget
p2 = gaugelib.DrawGauge2(root, max_value=300.0, min_value=0.0,
                        size=140, bg_col='black',
                        unit="psi", bg_sel=2)

start_btn = Button(root, text="START", width=8, height=2, 
                   bg="#4EA20E", fg="black",
                   font=('URW Gothic L', 16, 'bold'),
                   activebackground='#428C09', command=start)

stop_btn = Button(root, text="STOP", width=8, height=2, 
                   bg="#D9290B", fg="black",
                   font=('URW Gothic L', 16, 'bold'),
                   activebackground='#AE220B', command=stop)

path.place(x=100,y=90)
tank.place(x=570,y=137)
tank2.place(x=180,y=137)

p1.place(x=30,y=110)
p2.place(x=650,y=110)
start_btn.place(x=240, y=30)
stop_btn.place(x=400,y=30)

root.mainloop()


