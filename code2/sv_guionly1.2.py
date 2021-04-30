from tkinter import *
from PIL import ImageTk,Image
import sys
import time
import calendar
import gaugelib
import threading
import datetime as dt

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
#def read_gauge():


#Read Pressure Sensor 2
#def read_gauge2():


#Closing all valves
def  closeAll():
	print('Close all valves')


#Start the Program for first sequence
def start1():
	if (g_value <= 150) and (g_value >= 50):
		print('open valve 1 & 2')
		print('close valve 3 & 4')
	if (g_value < 50):
		closeAll()


#Start the Program for second sequence
def start2():
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
            placeTurbine1()
            arroway11()
            arroway21()
            arroway31()
            arroway41()
            time.sleep(0.1)
            placeTurbine2()
            arroway12()
            arroway22()
            arroway32()
            arroway42()
            time.sleep(0.1)
            start2()
            if switch == False:
            	if not arroway10() and arroway20():
	                break 
    t = threading.Thread(target=run)
    t.start()
    
def stop():
    print('System exited')
    global switch
    switch = False
    closeAll()

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
                        size=130, bg_col='black',
                        unit="psi", bg_sel=2)
#Inserting gauge widget
p2 = gaugelib.DrawGauge2(root, max_value=300.0, min_value=0.0,
                        size=130, bg_col='black',
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
p1.place(x=30,y=110)
p2.place(x=650,y=110)
start_btn.place(x=280, y=30)
stop_btn.place(x=420,y=30)

tank.place(x=570,y=137)
tank2.place(x=180,y=137)
#turbine.place(x=350,y=137)

root.mainloop()