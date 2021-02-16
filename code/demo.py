from tkinter import *
from tkinter import ttk
from tkinter import font
from PIL import ImageTk,Image
import sys
import time
import random
import gaugelib
import calendar
import threading
import datetime as dt
import RPi.GPIO as GPIO

switch = True

root = Tk()
root.geometry("800x420")
root.title("AIR COMPRESSOR CONTROL SYSTEM")

tabs = ttk.Notebook(root)
tabs.pack()

def select1():
    tabs.select(0)

def select2():
    tabs.select(1)

tab1 = Frame(tabs, width=800, height=420, bg='black')
tab2 = Frame(tabs, width=800, height=420, bg='black')
tab1.pack(fill="both", expand=1)
tab2.pack(fill="both", expand=1)
tabs.add(tab1, text="Refill", state='hidden')
tabs.add(tab2, text="Discharge")
# tabs.hide(0)
#tabs.hide(1)

##################################################################################
#                                                                                #
#                                                                                #
# # # # # # # # # # # # #    FIRST TAB OF INTERFACE    # # # # # # # # # # # # # #        
#                                                                                #
#                                                                                #
##################################################################################


bg = Image.open('images/latestbgrnd.png')
bgg = ImageTk.PhotoImage(bg)

labelbg = Label(tab1, image=bgg)
labelbg.place(x=0, y=-15, relwidth=1, relheight=1)

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
        

def choice(option):
    pop.destroy()

    if option == "yes":
        print("You Clicked Yes!")
        switchon()
    else:
        print("You Clicked No!!")

def messagebox():

    global pop
    pop = Toplevel(tab1)
    pop.title("Warning Message")
    pop.config(bg='white')
    pop.geometry("250x120")

    global warn
    warn = PhotoImage(file="images/warning.png")

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


def switchon():
    global switch
    switch = True
    print('System is running')
    # startSystem()
    step()
    anic1()
    
def switchoff():
    print('System exited')
    global switch
    switch = False
    #bstop()
    circlez()
    
def blink_led1():
    def run():
        while switch == True:
            circlez_1a()
            time.sleep(0.1)
            circlez_1b()
            time.sleep(0.1)
            if switch == False:
                break
    t = threading.Thread(target=run)
    t.start()

def on_led1():
    global switch
    switch = True
    print('led1 is on')
    blink_led1()


def blink_led2():
    def run():
        while switch == True:
            circlez_2a()
            time.sleep(0.1)
            circlez_2b()
            time.sleep(0.1)
            if switch == False:
                break
    t = threading.Thread(target=run)
    t.start()

def on_led2():
    global switch
    switch = True
    print('led2 is on')
    blink_led2()


def blink_path1():
    start = time.time()
    i = 10
    while (i > 0):
        i = 11 - (time.time() - start)
        tlabel.config(text=str(int(i))+" secs")
        print('led1 is blinking..')
        circlez_1a()
        time.sleep(0.1)
        circlez_1b()
        time.sleep(0.1)
        if (switch==False):
            break
       
 

def blink_path2():
    start = time.time()
    
    i = 10
    while (i > 0):
        i = 11 - (time.time() - start)
        tlabel1.config(text=str(int(i))+" secs")
        print('led2 is blinking..')
        circlez_2a()
        time.sleep(0.1)
        circlez_2b()
        time.sleep(0.1)
        if switch==False:
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

        
#Toggle Switch for Compressor 1
def toggle1():
    if led1_btn.config('text')[-1] == 'ON':
        led1_btn.config(text='OFF', image=offb, bg='black', borderwidth=0,
                        activebackground='black')
        print ("pressed true")
        on_led1()
    else:
        led1_btn.config(text='ON', image=onb, bg='black', borderwidth=0,
                        activebackground='black')
        switchoff()


#Toggle Switch for Compressor 2
def toggle2():
    if led2_btn.config('text')[-1] == 'ON':
        led2_btn.config(text='OFF', image=offb, bg='black', borderwidth=0,
                        activebackground='black')
        print ("pressed true")
        on_led2()
    else:
        led2_btn.config(text='ON', image=onb, bg='black', borderwidth=0,
                        activebackground='black')
        switchoff()
        
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
dance = Canvas(tab1, bg='black',width=425,height=265)
#Draw many many circles (put in a function)
circlez()

#Inserting Compressor Icon
ac = Image.open('images/aircompp.png')
res_ac = ac.resize((110, 110), Image.ANTIALIAS)
newac = ImageTk.PhotoImage(res_ac)
airComp = Label(tab1, image=newac, bg='black')

#Inserting second Compressor Icon
ac1 = Image.open('images/aircompp.png')
res_ac1 = ac1.resize((110, 110), Image.ANTIALIAS)
newac1 = ImageTk.PhotoImage(res_ac1)
airComp1 = Label(tab1, image=newac1, bg='black')

#Inserting Tank Icon
gt = Image.open('images/tank.png')
res_gt = gt.resize((54, 220), Image.ANTIALIAS)
newgt = ImageTk.PhotoImage(res_gt)
tank = Label(tab1, image=newgt, bg='black')

#Inserting Start Button Image
sb = Image.open('images/start.png')
res_sb = sb.resize((167, 70), Image.ANTIALIAS)
newsb = ImageTk.PhotoImage(res_sb)

#Inserting Stop Button Image
stopb = Image.open('images/stop.png')
res_stopb = stopb.resize((167, 70), Image.ANTIALIAS)
newstopb = ImageTk.PhotoImage(res_stopb)

#Inserting ON Button Image
on = Image.open('images/on.png')
res_on = on.resize((80, 80), Image.ANTIALIAS)
onb = ImageTk.PhotoImage(res_on)

#Inserting OFF Button Image
off = Image.open('images/off.png')
res_off = off.resize((80, 80), Image.ANTIALIAS)
offb = ImageTk.PhotoImage(res_off)

#Inserting discharge Button Image
db = Image.open('images/discharge.png')
res_db = db.resize((150, 30), Image.ANTIALIAS)
newdb = ImageTk.PhotoImage(res_db)

#Inserting clock
clock1 = Clock(tab1)
clock1.configure(bg='black',fg='white',font=("Quicksand",16, 'bold'))
#Adding date
date = Label(tab1, text=f"{dt.datetime.now():%a, %b %d %Y}",
             fg="white", bg="black", font=("helvetica",14))


#START Button
start_btn = Button(tab1, image=newsb, command=messagebox, 
                    borderwidth=0, bg='black',activebackground='black')

stop_btn = Button(tab1, image=newstopb, command=switchoff,
                    borderwidth=0, bg='black',activebackground='black')


#ON_LED1 Toggle Button
led1_btn = Button(tab1, text='ON', image=onb, command=toggle1,
                    borderwidth=0, bg='black',activebackground='black')

#ON_LED2 Toggle Button
led2_btn = Button(tab1, text='ON', image=onb, command=toggle2,
                    borderwidth=0, bg='black',activebackground='black')

#Inserting progress bar
percent = StringVar()
pbar = ttk.Progressbar(tab1, orient=VERTICAL,
                       length = 220,mode='determinate')
#Inserting progress bar label
plabel = Label(tab1, textvariable=percent, font=('Quicksand',10),
                bg='black', fg='white')


#Inserting exit button
exit_btn = Button(tab1, text="Quit", width=4, height=1,
                  bg="black", fg="white",
                  command=lambda root=root:quit(root))

#Inserting timer label
tlabel = Label(tab1, text=' ',
              font=('Quicksand', 14),
              bg='black', fg='white')

#Inserting timer1 label
tlabel1 = Label(tab1, text=' ',
              font=('Quicksand', 14),
          bg='black', fg='white' )

#Inserting compressor 1 label
clabel1 = Label(tab1, text='C1', font=('URW Gothic L', 14, 'bold'),
          bg='black', fg='white' )


#Inserting compressor 2 label
clabel2 = Label(tab1, text='C2', font=('URW Gothic L', 14, 'bold'),
          bg='black', fg='white' )

btab2 = Button(tab1, image=newdb, command=select2,
        borderwidth=0, bg='black',activebackground='black')


#.................................#
#..DISPLAYING VARIABLE ON SCREEN..#
#.................................#

btab2.place(x=635,y=70)
date.place(x=260,y=70)
clock1.place(x=425,y=70)

start_btn.place(x=15,y=225)
stop_btn.place(x=15,y=305)
led1_btn.place(x=680,y=140)
led2_btn.place(x=680,y=260)

dance.place(x=200,y=105)
plabel.place(x=580,y=115)
pbar.place(x=590,y=140)
tank.place(x=520,y=140)
airComp.place(x=213,y=117)
clabel1.place(x=262,y=172) 
tlabel.place(x=330,y=195)
airComp1.place(x=213,y=252)
clabel2.place(x=262,y=307) 
tlabel1.place(x=330,y=325) 

exit_btn.place(x=750,y=360)



#................................................................................#
##################################################################################
#                                                                                #
#                                                                                #
# # # # # # # # # # # # #    SECOND TAB OF INTERFACE   # # # # # # # # # # # # # #        
#                                                                                #
#                                                                                #
##################################################################################
#................................................................................#

#Adding background to page
bg1 = Image.open('images/latestbgrnd2.png')
bgg1 = ImageTk.PhotoImage(bg1)

labelbg1 = Label(tab2, image=bgg1)
labelbg1.place(x=0, y=0, relwidth=1, relheight=1)

svalve = 25
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(svalve,GPIO.OUT)


g_value=0
ga_value=0
f=0
g=0

def read_gauge():
    def run():
        global f
        global g_value
        while (g_value<100):
            time.sleep(1.45036)
            g_value+=1
            f+=1
            if f>100:
                f=0
            p1.set_value(int(g_value))
            root.update_idletasks()
            #root.after(100,read_gauge)
            if(g_value==100 or switch==False):
                break
    t = threading.Thread(target=run)
    t.start()

def read_gauge2():
    def run():        
        global g
        global ga_value
        while (ga_value<4350):
            time.sleep(0.1)
            ga_value+=1
            g+=1
            if g>4350:
                g=0
            p2.set_value(int(ga_value))
            root.update_idletasks()
            #root.after(100,read_gauge)
            if(ga_value==4350 or switch==False):
                break
    t = threading.Thread(target=run)
    t.start()
    
    
def start_valve():
    def run():
        while switch == True:
            circles1()
            time.sleep(0.1)
            circles2()
            time.sleep(0.1)
            if switch == False:
                break
    t = threading.Thread(target=run)
    t.start()

def open_valve():
    print('Valve is open')
    global switch
    switch = True
    GPIO.output(svalve, True)
    start_valve()
    read_gauge()
    read_gauge2()

def close_valve():
    print('Valve is close')
    global switch
    switch = False
    GPIO.output(svalve, False)
    circles()

#Toggle Switch for Valve
def toggle_valve():
    if valve_btn.config('text')[-1] == 'open':
        valve_btn.config(text='close', image=newcb, bg='black', borderwidth=0,
                        activebackground='black')
        print ("pressed true")
        open_valve()
    else:
        valve_btn.config(text='open', image=newob, bg='black', borderwidth=0,
                        activebackground='black')
        close_valve()


def circles():
    s1 = rock.create_oval(105,40,115,50,fill='white')
    s2 = rock.create_oval(120,40,130,50,fill='white')
    s3 = rock.create_oval(135,40,145,50,fill='white')
    s4 = rock.create_oval(150,40,160,50,fill='white')
    s5 = rock.create_oval(165,40,175,50,fill='white')
    s6 = rock.create_oval(180,40,190,50,fill='white')
    s7 = rock.create_oval(180,55,190,65,fill='white')
    s8 = rock.create_oval(180,70,190,80,fill='white')
    s9 = rock.create_oval(180,85,190,95,fill='white')
    s10 = rock.create_oval(180,100,190,110,fill='white')
    s11 = rock.create_oval(180,115,190,125,fill='white')
    s12 = rock.create_oval(180,130,190,140,fill='white')
    s13 = rock.create_oval(180,145,190,155,fill='white')
    s14 = rock.create_oval(180,160,190,170,fill='white')
    s15 = rock.create_oval(180,175,190,185,fill='white')
    s16 = rock.create_oval(180,190,190,200,fill='white')
    s17 = rock.create_oval(195,190,205,200,fill='white')
    s18 = rock.create_oval(210,190,220,200,fill='white')
    s19 = rock.create_oval(225,190,235,200,fill='white')

def circles1():
    s1 = rock.create_oval(105,40,115,50,fill='orange')
    s2 = rock.create_oval(120,40,130,50,fill='white')
    s3 = rock.create_oval(135,40,145,50,fill='orange')
    s4 = rock.create_oval(150,40,160,50,fill='white')
    s5 = rock.create_oval(165,40,175,50,fill='orange')
    s6 = rock.create_oval(180,40,190,50,fill='white')
    s7 = rock.create_oval(180,55,190,65,fill='orange')
    s8 = rock.create_oval(180,70,190,80,fill='white')
    s9 = rock.create_oval(180,85,190,95,fill='orange')
    s10 = rock.create_oval(180,100,190,110,fill='white')
    s11 = rock.create_oval(180,115,190,125,fill='orange')
    s12 = rock.create_oval(180,130,190,140,fill='white')
    s13 = rock.create_oval(180,145,190,155,fill='orange')
    s14 = rock.create_oval(180,160,190,170,fill='white')
    s15 = rock.create_oval(180,175,190,185,fill='orange')
    s16 = rock.create_oval(180,190,190,200,fill='white')
    s17 = rock.create_oval(195,190,205,200,fill='orange')
    s18 = rock.create_oval(210,190,220,200,fill='white')
    s19 = rock.create_oval(225,190,235,200,fill='orange')

def circles2():
    s1 = rock.create_oval(105,40,115,50,fill='white')
    s2 = rock.create_oval(120,40,130,50,fill='orange')
    s3 = rock.create_oval(135,40,145,50,fill='white')
    s4 = rock.create_oval(150,40,160,50,fill='orange')
    s5 = rock.create_oval(165,40,175,50,fill='white')
    s6 = rock.create_oval(180,40,190,50,fill='orange')
    s7 = rock.create_oval(180,55,190,65,fill='white')
    s8 = rock.create_oval(180,70,190,80,fill='orange')
    s9 = rock.create_oval(180,85,190,95,fill='white')
    s10 = rock.create_oval(180,100,190,110,fill='orange')
    s11 = rock.create_oval(180,115,190,125,fill='white')
    s12 = rock.create_oval(180,130,190,140,fill='orange')
    s13 = rock.create_oval(180,145,190,155,fill='white')
    s14 = rock.create_oval(180,160,190,170,fill='orange')
    s15 = rock.create_oval(180,175,190,185,fill='white')
    s16 = rock.create_oval(180,190,190,200,fill='orange')
    s17 = rock.create_oval(195,190,205,200,fill='white')
    s18 = rock.create_oval(210,190,220,200,fill='orange')
    s19 = rock.create_oval(225,190,235,200,fill='white')


#########################################################
#                                                       #
#                    ADDING WIDGETS                     #
#                                                       #
#########################################################
#

#Inserting clock
clock2 = Clock(tab2)
clock2.configure(bg='black',fg='white',font=("Quicksand",16, 'bold'))
#Adding date
date2 = Label(tab2, text=f"{dt.datetime.now():%a, %b %d %Y}",
             fg="white", bg="black", font=("helvetica",14))

#Inserting frame for animation
rock = Canvas(tab2, bg='black',width=400,height=265)
circles()

#Inserting Tank Image
gt2 = Image.open('images/tank2.png')
res_gt2 = gt2.resize((54, 220), Image.ANTIALIAS)
newgt2 = ImageTk.PhotoImage(res_gt2)
tank2 = Label(tab2, image=newgt2, bg='black')

#Inserting Generator Image
gn = Image.open('images/generator.png')
res_gn = gn.resize((150, 150), Image.ANTIALIAS)
newgn = ImageTk.PhotoImage(res_gn)
generator = Label(tab2, image=newgn, bg='black')

#Inserting open Button Image
ob = Image.open('images/open.png')
res_ob = ob.resize((100, 100), Image.ANTIALIAS)
newob = ImageTk.PhotoImage(res_ob)

#Inserting close Button Image
cb = Image.open('images/close.png')
res_cb = cb.resize((100, 100), Image.ANTIALIAS)
newcb = ImageTk.PhotoImage(res_cb)

#Inserting discharge Button Image
rb = Image.open('images/refill.png')
res_rb = rb.resize((150, 30), Image.ANTIALIAS)
newrb = ImageTk.PhotoImage(res_rb)

#Inserting gauge widget
p1 = gaugelib.DrawGauge2(tab2, max_value=300.0, min_value=0.0,
                        size=140, bg_col='black',
                        unit="bar", bg_sel=2)
#Inserting gauge widget
p2 = gaugelib.DrawGauge2(tab2, max_value=4350.0, min_value=0.0,
                        size=140, bg_col='black',
                        unit="psi", bg_sel=2)

btab1 = Button(tab2, image=newrb, command=select1,
                borderwidth=0, bg='black',activebackground='black')

#ON_LED1 Toggle Button
valve_btn = Button(tab2, text='open', image=newob, command=toggle_valve,
                    bg='black', borderwidth=0, activebackground='black')


##....DISPLAYING VARIABLE ON SCREEN.....##
#
rock.place(x=380,y=110)
btab1.place(x=635,y=70)
date2.place(x=260,y=70)
clock2.place(x=425,y=70)
tank2.place(x=427, y=137)
generator.place(x=620,y=217)
valve_btn.place(x=25,y=200)

p1.place(x=230,y=250)
p2.place(x=230,y=110)

root.mainloop()

