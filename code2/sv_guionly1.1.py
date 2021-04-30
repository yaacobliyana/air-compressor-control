from tkinter import *
import sys
import time
import gaugelib
import threading


switch = True
g_value=0
ga_value=0
f=0
g=0

root = Tk()
root.geometry("800x420")
root.title("AIR COMPRESSOR CONTROL SYSTEM")
root.configure(bg='black')

#Read Pressure Sensor 1
def read_gauge():
    def run():
        global f
        global g_value
        global switch
        while (g_value<300):
            time.sleep(0.5)
            g_value+=1
            f+=1
            if f>300:
                f=0
            p1.set_value(int(g_value))
            root.update_idletasks()
            #root.after(100,read_gauge)
            if(g_value==300 or switch==False):
                break
    t = threading.Thread(target=run)
    t.start()

#Read Pressure Sensor 2
def read_gauge2():
    def run():
        global g
        global ga_value
        global switch
        while (ga_value<300):
            time.sleep(0.5)
            ga_value+=1
            g+=1
            if g>300:
                g=0
            p2.set_value(int(ga_value))
            root.update_idletasks()
            #root.after(100,read_gauge)
            if(ga_value==300 or switch==False):
                break
    t = threading.Thread(target=run)
    t.start()

def  closeAll():
	print('Close all valves')


#Start the Program for first sequence
def start1():
	read_gauge()
	if (g_value <= 150) and (g_value >= 50):
		print('open valve 1 & 2')
		print('close valve 3 & 4')
	if (g_value < 50):
		closeAll()


#Start the Program for second sequence
def start2():
	read_gauge2()
	if (g_value <= 150) and (g_value >= 50):
		print('open valve 3 & 4')
		print('close valve 1 & 2')
	if (g_value < 50):
		closeAll()


def start():
    def run():
        global switch
        switch = True
        while switch == True:
            start1()
            start2()
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