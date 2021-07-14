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

# bg = Image.open('images/bgrnd.png')
# bgg = ImageTk.PhotoImage(bg)
# labelbg = Label(root, image=bgg)
# labelbg.place(x=0, y=0, relwidth=1, relheight=1)

#Read Pressure Sensor 1
#def read_gauge():


#Read Pressure Sensor 2
#def read_gauge2():


#Closing all valves
def  closeAll():
	print('Close all valves')
	placeVR1_on()
	placeVR2_on()
	placeVG1_off()
	placeVG2_off()
	arroway10()
	arroway20()


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

def valve_path1():
	def run():
		while switch == True:
			arroway11()
			time.sleep(0.25)
			arroway12()
			time.sleep(0.25)
			if switch == False:
				break
	t = threading.Thread(target=run)
	t.start()

def valve_path2():
	def run():
		while switch == True:
			arroway21()
			time.sleep(0.25)
			arroway22()
			time.sleep(0.25)
			if switch == False:
				break
	t = threading.Thread(target=run)
	t.start()

def start():
    def run():
        global switch
        switch = True
        while switch == True:
            start1()
            placeVG1_on()
            placeVG1_off()
            valve_path1()
            if switch == False:
            	if not closeAll():
	                break 
    t = threading.Thread(target=run)
    t.start()


def stop():
    print('System exited')
    global switch
    global blink
    switch = False
    blink = False
    closeAll()

####------ ADDING WIDGETS ------####

#Inserting frame for animation
path = Canvas(root, bg='black', width=600, height=300, 
				bd=0, highlightthickness=0, relief='ridge')


#Inserting ON valve indicator (LIGHT ON) Image
vi_lon = Image.open('images/valveon1.png')
res_vi_lon = vi_lon.resize((30, 30), Image.ANTIALIAS)
newvi_lon = ImageTk.PhotoImage(res_vi_lon)

#Inserting ON valve indicator (LIGHT OFF) Image
vi_lof = Image.open('images/valveon2.png')
res_vi_lof = vi_lof.resize((30, 30), Image.ANTIALIAS)
newvi_lof = ImageTk.PhotoImage(res_vi_lof)

def placeVG1_off():
	vonl = Label(root, image=newvi_lof, bg='black')
	vonl.place(x=242,y=85) 
	vonl = Label(root, image=newvi_lof, bg='black')
	vonl.place(x=492,y=179)

def placeVG2_off():
	vonl = Label(root, image=newvi_lof, bg='black')
	vonl.place(x=492,y=85) 
	vonl = Label(root, image=newvi_lof, bg='black')
	vonl.place(x=242,y=179)

def placeVG1_on():
	vonl = Label(root, image=newvi_lon, bg='black')
	vonl.place(x=242,y=85) 
	vonl = Label(root, image=newvi_lon, bg='black')
	vonl.place(x=492,y=179) 

def placeVG2_on():
	vonl = Label(root, image=newvi_lon, bg='black')
	vonl.place(x=492,y=85) 
	vonl = Label(root, image=newvi_lon, bg='black')
	vonl.place(x=242,y=179) 


placeVG1_off()
placeVG2_off()

#Inserting OFF valve indicator (LIGHT ON) Image
vo_lon = Image.open('images/valveoff1.png')
res_vo_lon = vo_lon.resize((30, 30), Image.ANTIALIAS)
newvo_lon = ImageTk.PhotoImage(res_vo_lon)

#Inserting OFF valve indicator (LIGHT OFF) Image
vo_lof = Image.open('images/valveoff2.png')
res_vo_lof = vo_lof.resize((30, 30), Image.ANTIALIAS)
newvo_lof = ImageTk.PhotoImage(res_vo_lof)

def placeVR1_off():
	voffl = Label(root, image=newvo_lof, bg='black')
	voffl.place(x=273,y=85)
	voffl = Label(root, image=newvo_lof, bg='black')
	voffl.place(x=523,y=179)

def placeVR2_off():
	voffl = Label(root, image=newvo_lof, bg='black')
	voffl.place(x=273,y=179)
	voffl = Label(root, image=newvo_lof, bg='black')
	voffl.place(x=523,y=85)

def placeVR1_on():
	voffl = Label(root, image=newvo_lon, bg='black')
	voffl.place(x=273,y=85)
	voffl = Label(root, image=newvo_lon, bg='black')
	voffl.place(x=523,y=179)

def placeVR2_on():
	voffl = Label(root, image=newvo_lon, bg='black')
	voffl.place(x=523,y=85)
	voffl = Label(root, image=newvo_lon, bg='black')
	voffl.place(x=273,y=179)


placeVR1_on()
placeVR2_on()

#Inserting Arrow Image 1
ar = Image.open('images/narrow.png')
res_ar = ar.resize((100, 24), Image.ANTIALIAS)
newar = ImageTk.PhotoImage(res_ar)

#Inserting Arrow Image 2
ar1 = Image.open('images/narrow1.png')
res_ar1 = ar1.resize((100, 24), Image.ANTIALIAS)
newar1 = ImageTk.PhotoImage(res_ar1)

#Inserting Arrow Image 3
ar2 = Image.open('images/narrow2.png')
res_ar2 = ar2.resize((100, 24), Image.ANTIALIAS)
newar2 = ImageTk.PhotoImage(res_ar2)

#Inserting Arrow Image 4
af = Image.open('images/narrowf.png')
res_af = af.resize((100, 24), Image.ANTIALIAS)
newaf = ImageTk.PhotoImage(res_af)

#Inserting Arrow Image 5
af1 = Image.open('images/narrowf1.png')
res_af1 = af1.resize((100, 24), Image.ANTIALIAS)
newaf1 = ImageTk.PhotoImage(res_af1)

#Inserting Arrow Image 6
af2 = Image.open('images/narrowf2.png')
res_af2 = af2.resize((100, 24), Image.ANTIALIAS)
newaf2 = ImageTk.PhotoImage(res_af2)

def arroway10():
	arrow = Label(root, image=newar, bg='black')
	arrow.place(x=230,y=120)
	arrow = Label(root, image=newar, bg='black')
	arrow.place(x=470,y=154)

def arroway11():
	arrow1 = Label(root, image=newar1, bg='black')
	arrow1.place(x=470,y=154)
	arrow1 = Label(root, image=newar1, bg='black')
	arrow1.place(x=230,y=120)

def arroway12():
	arrow2 = Label(root, image=newar2, bg='black')
	arrow2.place(x=230,y=120)	
	arrow2 = Label(root, image=newar2, bg='black')
	arrow2.place(x=470,y=154)

def arroway20():
	arrow = Label(root, image=newaf, bg='black')
	arrow.place(x=470,y=120)
	arrow = Label(root, image=newaf, bg='black')
	arrow.place(x=230,y=154)

def arroway21():
	arrow1 = Label(root, image=newaf1, bg='black')
	arrow1.place(x=470,y=120)
	arrow1 = Label(root, image=newaf1, bg='black')
	arrow1.place(x=230,y=154)

def arroway22():
	arrow2 = Label(root, image=newaf2, bg='black')
	arrow2.place(x=470,y=120)
	arrow2 = Label(root, image=newaf2, bg='black')
	arrow2.place(x=230,y=154)

arroway10()
arroway20()

#Inserting Water Flow Image
w1 = Image.open('images/waterflow_scircle10.png')
res_w1 = w1.resize((140, 20), Image.ANTIALIAS)
neww1 = ImageTk.PhotoImage(res_w1)

#Inserting Water Flow Image
w2 = Image.open('images/waterflow_scircle20.png')
res_w2 = w2.resize((20, 35), Image.ANTIALIAS)
neww2 = ImageTk.PhotoImage(res_w2)

def flow10():
	wflow10 = Label(root, image=neww1, bg='black')
	wflow10.place(x=195,y=329)
	wflow10 = Label(root, image=neww1, bg='black')
	wflow10.place(x=465,y=329)

def flow20():
	wflow20 = Label(root, image=neww2, bg='black')
	wflow20.place(x=194,y=294)
	wflow20 = Label(root, image=neww2, bg='black')
	wflow20.place(x=587,y=294)

flow10()
flow20()


#Inserting Tank Image
gt = Image.open('images/tank.png')
res_gt = gt.resize((44, 180), Image.ANTIALIAS)
newgt = ImageTk.PhotoImage(res_gt)
tank = Label(root, image=newgt, bg='black')

#Inserting Tank 2 Image
gt2 = Image.open('images/tank2.png')
res_gt2 = gt2.resize((44, 180), Image.ANTIALIAS)
newgt2 = ImageTk.PhotoImage(res_gt2)
tank2 = Label(root, image=newgt2, bg='black')

#Inserting Turbine Label Image
tt = Image.open('images/wturbine.png')
res_tt = tt.resize((130, 84), Image.ANTIALIAS)
newtt = ImageTk.PhotoImage(res_tt)
turbine = Label(root, image=newtt, bg='black')

#Inserting Water Pump Label Image
wwp = Image.open('images/wwaterpump.png')
res_wwp = wwp.resize((130, 84), Image.ANTIALIAS)
newwwp = ImageTk.PhotoImage(res_wwp)
waterpumpLabel = Label(root, image=newwwp, bg='black')

#Inserting Water Pump Image
wp = Image.open('images/waterpump.png')
res_wp = wp.resize((100, 64), Image.ANTIALIAS)
newwp = ImageTk.PhotoImage(res_wp)
waterpump = Label(root, image=newwp, bg='black')

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
                        size=130, bg_col='black',
                        unit="psi", bg_sel=2)
#Inserting gauge widget
p2 = gaugelib.DrawGauge2(root, max_value=300.0, min_value=0.0,
                        size=130, bg_col='black',
                        unit="psi", bg_sel=2)

#START Button
start_btn = Button(root, image=newsb, command=start, 
                    borderwidth=0, bg='black',activebackground='black')

stop_btn = Button(root, image=newstb, command=stop, 
                    borderwidth=0, bg='black',activebackground='black')

path.place(x=100,y=90)
p1.place(x=25,y=140)
p2.place(x=650,y=140)
start_btn.place(x=250, y=20)
stop_btn.place(x=410,y=20)

tank.place(x=576,y=110)
tank2.place(x=180,y=110)
turbine.place(x=335,y=107)
waterpumpLabel.place(x=335,y=300)

#waterpump.place(x=10,y=300)

root.mainloop()