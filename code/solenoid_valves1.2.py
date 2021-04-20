from tkinter import *
import sys
import time
import gaugelib
import threading
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

def start():
    def run():
        global switch
        switch = True
        while switch == True:
            start1()
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

####------ ADDING WIDGETS ------####

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

p1.place(x=320,y=250)
p2.place(x=320,y=110)
start_btn.place(x=240, y=30)
stop_btn.place(x=400,y=30)

root.mainloop()


