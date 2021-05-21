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

bg = Image.open('images/bgrnd.png')
bgg = ImageTk.PhotoImage(bg)

labelbg = Label(root, image=bgg)
labelbg.place(x=0, y=0, relwidth=1, relheight=1)

def start():
    global switch
    switch = True
    read_gauge()
    start2()
#     read_gauge2()
#     startAni2()
    #start2()

#Read Pressure Sensor 1
def read_gauge():
    def run():
        global p1_value
        global p2_value
        global switch
        switch = True
        while switch == True:
            #time.sleep(0.1)
            v1 = chan0.voltage
            v2 = chan1.voltage
            p1_value = (78*(v1-0.4787))
            p2_value = (78*(v2-0.4787))
            p1.set_value(int(p1_value))
            p2.set_value(int(p2_value))
            #print('ADC Voltage 1: ' + str(chan0.voltage) + 'V')
            print('Pressure 1: ' + str(int(p1_value)) + 'bar')
            print('Pressure 2: ' + str(int(p2_value)) + 'bar')
            root.update_idletasks()
            start1()
            #root.after(100,read_gauge)
            if switch == False:
                if not stop():
                    break
            if switch == True:
                if not start1():
                    continue
    t = threading.Thread(target=run)
    t.start()


#Start the Program for first sequence
def start1():
    if (p2_value < 50):
        if (p1_value <= 150) and (p1_value >= 50):
            GPIO.output(13, False)
            GPIO.output(19, False)
            GPIO.output(26, True)
            GPIO.output(16, True)
            print('open valve 1 & 2')
            print('close valve 3 & 4')
        elif (p1_value < 50):
            closeAll()
    if (p1_value < 50):
        if (p2_value <= 150) and (p2_value >= 50):
            GPIO.output(13, True)
            GPIO.output(19, True)
            GPIO.output(26, False)
            GPIO.output(16, False)
            print('open valve 3 & 4')
            print('close valve 1 & 2')
        elif (p2_value < 50):
            closeAll()
    

def start2():
    if (p2_value < 50):
        if (p1_value <= 150) and (p1_value >= 50):
            placeVon1_on()
            placeVof1_off()
            valve_path1()
            turbineSpin()
        elif (p1_value < 50):
            closeAll()
    if (p2_value <= 150) and (p2_value >= 50):
        if (p1_value < 50):
            placeVon2_on()
            placeVof2_off()
            valve_path2()
            turbineSpin()
        elif (p1_value <= 150) and (p1_value >= 50):
            closeAll()

def startAni1():
    if (p1_value <= 150) and (p1_value >= 50):
        placeVon1_on()
        placeVof1_off()
        valve_path1()
        turbineSpin()
    elif (p1_value < 50):
        stop()
#         startAni2()


def startAni2():
    if (p2_value <= 150) and (p2_value >= 50):
        placeVon2_on()
        placeVof2_off()
        valve_path2()
        turbineSpin()
    elif (p2_value <= 50):
        stop()
#         startAni1()


def stop():
    print('System exited')
    global switch
    global blink
    global blink1
    global blink2
    switch = False
    blink = False
    blink1 = False
    blink2 = False
    closeAll()

def closeAll():
    GPIO.output(13, True)
    GPIO.output(19, True)
    GPIO.output(26, True)
    GPIO.output(16, True)
    print('Close all valves')
    placeVof1_on()
    placeVof2_on()
    placeVon1_off()
    placeVon2_off()
    arroway10()
    arroway20()

def valve_path1():
    def run1():
        global blink1
        blink1 = True
        while blink1 == True:
            arroway11()
            time.sleep(0.25)
            arroway12()
            time.sleep(0.25)
            if blink1 == False:
                break
    t1 = threading.Thread(target=run1)
    t1.start()

def valve_path2():
    def run2():
        global blink2
        blink2 = True
        while blink2 == True:
            arroway21()
            time.sleep(0.25)
            arroway22()
            time.sleep(0.25)
            if blink2 == False:
                break
    t2 = threading.Thread(target=run2)
    t2.start()

def turbineSpin():
    def run3():
        global blink
        blink = True
        while blink == True:
            placeTurbine1()
            time.sleep(0.1)
            placeTurbine2()
            time.sleep(0.1)
            if blink == False:
                break
    t3=threading.Thread(target=run3)
    t3.start()

    

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

#Inserting ON valve indicator (LIGHT ON) Image
vi_lon = Image.open('images/valveon1.png')
res_vi_lon = vi_lon.resize((35, 35), Image.ANTIALIAS)
newvi_lon = ImageTk.PhotoImage(res_vi_lon)

#Inserting ON valve indicator (LIGHT OFF) Image
vi_lof = Image.open('images/valveon2.png')
res_vi_lof = vi_lof.resize((35, 35), Image.ANTIALIAS)
newvi_lof = ImageTk.PhotoImage(res_vi_lof)

def placeVon1_off():
    vonl = Label(root, image=newvi_lof, bg='black')
    vonl.place(x=242,y=95)
    vonl = Label(root, image=newvi_lof, bg='black')
    vonl.place(x=492,y=245)

def placeVon2_off():
    vonl = Label(root, image=newvi_lof, bg='black')
    vonl.place(x=492,y=95)
    vonl = Label(root, image=newvi_lof, bg='black')
    vonl.place(x=242,y=245)

def placeVon1_on():
    vonl = Label(root, image=newvi_lon, bg='black')
    vonl.place(x=242,y=95)
    vonl = Label(root, image=newvi_lon, bg='black')
    vonl.place(x=492,y=245)

def placeVon2_on():
    vonl = Label(root, image=newvi_lon, bg='black')
    vonl.place(x=492,y=95)
    vonl = Label(root, image=newvi_lon, bg='black')
    vonl.place(x=242,y=245)


placeVon1_off()
placeVon2_off()

#Inserting OFF valve indicator (LIGHT ON) Image
vo_lon = Image.open('images/valveoff1.png')
res_vo_lon = vo_lon.resize((35, 35), Image.ANTIALIAS)
newvo_lon = ImageTk.PhotoImage(res_vo_lon)

#Inserting OFF valve indicator (LIGHT OFF) Image
vo_lof = Image.open('images/valveoff2.png')
res_vo_lof = vo_lof.resize((35, 35), Image.ANTIALIAS)
newvo_lof = ImageTk.PhotoImage(res_vo_lof)

def placeVof1_off():
    voffl = Label(root, image=newvo_lof, bg='black')
    voffl.place(x=278,y=95)
    voffl = Label(root, image=newvo_lof, bg='black')
    voffl.place(x=528,y=245)

def placeVof2_off():
    voffl = Label(root, image=newvo_lof, bg='black')
    voffl.place(x=278,y=245)
    voffl = Label(root, image=newvo_lof, bg='black')
    voffl.place(x=528,y=95)

def placeVof1_on():
    voffl = Label(root, image=newvo_lon, bg='black')
    voffl.place(x=278,y=95)
    voffl = Label(root, image=newvo_lon, bg='black')
    voffl.place(x=528,y=245)

def placeVof2_on():
    voffl = Label(root, image=newvo_lon, bg='black')
    voffl.place(x=528,y=95)
    voffl = Label(root, image=newvo_lon, bg='black')
    voffl.place(x=278,y=245)


placeVof1_on()
placeVof2_on()

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
ar = Image.open('images/narrow.png')
res_ar = ar.resize((110, 35), Image.ANTIALIAS)
newar = ImageTk.PhotoImage(res_ar)

#Inserting Arrow Image
ar1 = Image.open('images/narrow1.png')
res_ar1 = ar1.resize((110, 35), Image.ANTIALIAS)
newar1 = ImageTk.PhotoImage(res_ar1)

#Inserting Arrow Image
ar2 = Image.open('images/narrow2.png')
res_ar2 = ar2.resize((110, 35), Image.ANTIALIAS)
newar2 = ImageTk.PhotoImage(res_ar2)

#Inserting Arrow Image
af = Image.open('images/narrowf.png')
res_af = af.resize((110, 35), Image.ANTIALIAS)
newaf = ImageTk.PhotoImage(res_af)

#Inserting Arrow Image
af1 = Image.open('images/narrowf1.png')
res_af1 = af1.resize((110, 35), Image.ANTIALIAS)
newaf1 = ImageTk.PhotoImage(res_af1)

#Inserting Arrow Image
af2 = Image.open('images/narrowf2.png')
res_af2 = af2.resize((110, 35), Image.ANTIALIAS)
newaf2 = ImageTk.PhotoImage(res_af2)

def arroway10():
    arrow = Label(root, image=newar, bg='black')
    arrow.place(x=235,y=140)
    arrow = Label(root, image=newar, bg='black')
    arrow.place(x=460,y=210)

def arroway11():
    arrow1 = Label(root, image=newar1, bg='black')
    arrow1.place(x=460,y=210)
    arrow1 = Label(root, image=newar1, bg='black')
    arrow1.place(x=235,y=140)

def arroway12():
    arrow2 = Label(root, image=newar2, bg='black')
    arrow2.place(x=235,y=140)   
    arrow2 = Label(root, image=newar2, bg='black')
    arrow2.place(x=460,y=210)

def arroway20():
    arrow = Label(root, image=newaf, bg='black')
    arrow.place(x=460,y=140)
    arrow = Label(root, image=newaf, bg='black')
    arrow.place(x=235,y=210)

def arroway21():
    arrow1 = Label(root, image=newaf1, bg='black')
    arrow1.place(x=460,y=140)
    arrow1 = Label(root, image=newaf1, bg='black')
    arrow1.place(x=235,y=210)

def arroway22():
    arrow2 = Label(root, image=newaf2, bg='black')
    arrow2.place(x=460,y=140)
    arrow2 = Label(root, image=newaf2, bg='black')
    arrow2.place(x=235,y=210)

arroway10()
arroway20()

#Inserting Start Button Image
sb = Image.open('images/start2.png')
res_sb = sb.resize((150, 51), Image.ANTIALIAS)
newsb = ImageTk.PhotoImage(res_sb)

#Inserting Stop Button Image
stb = Image.open('images/stop2.png')
res_stb = stb.resize((150, 51), Image.ANTIALIAS)
newstb = ImageTk.PhotoImage(res_stb)

#Inserting gauge widget
p1 = gaugelib.DrawGauge2(root, max_value=300.0, min_value=0.0,
                        size=140, bg_col='black',
                        unit="bar", bg_sel=2)
#Inserting gauge widget
p2 = gaugelib.DrawGauge2(root, max_value=300.0, min_value=0.0,
                        size=140, bg_col='black',
                        unit="bar", bg_sel=2)

#START Button
start_btn = Button(root, image=newsb, command=start, 
                    borderwidth=0, bg='black',activebackground='black')

stop_btn = Button(root, image=newstb, command=stop, 
                    borderwidth=0, bg='black',activebackground='black')

path.place(x=100,y=90)
tank.place(x=570,y=137)
tank2.place(x=180,y=137)

p1.place(x=25,y=140)
p2.place(x=650,y=140)
start_btn.place(x=250, y=340)
stop_btn.place(x=410,y=340)

root.mainloop()


