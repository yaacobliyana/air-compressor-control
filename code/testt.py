from tkinter import *
import threading
import time
from PIL import ImageTk,Image

switch = True

root = Tk()
root.geometry("800x420")
root.title("LED TEST")
root.configure(bg='black')

#Inserting Compressor Icon
ac = Image.open('airComp.png')
res_ac = ac.resize((105, 100), Image.ANTIALIAS)
newac = ImageTk.PhotoImage(res_ac)
airComp = Label(root, image=newac, bg='black')
airComp.place(x=220,y=140)

#Inserting Compressor Icon
ac0 = Image.open('airComp1.png')
res_ac0 = ac0.resize((105, 100), Image.ANTIALIAS)
newac0 = ImageTk.PhotoImage(res_ac0)
airComp0 = Label(root, image=newac0, bg='black')

def blink_c1():
    def run():
        i=0
        while (i<1000):
            airComp0.place(x=220,y=140)
            time.sleep(0.5)
            airComp.place(x=220,y=140)
            time.sleep(0.5)
            if (i==1000):
                break

    t=threading.Thread(target=run)
    t.start()

blink_c1()    

root.mainloop()