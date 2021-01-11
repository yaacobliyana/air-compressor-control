from tkinter import *
from tkinter import font

root = Tk()
root.geometry("800x420")
root.title("LED TEST")
root.configure(bg='black')

font.families()

start_btn = Button(root, text="START", width=8, height=2, 
                   bg="#4EA20E", fg="black",
                   font=('URW Gothic L', 16, 'bold'),
                   activebackground='#428C09'
                   )
stop_btn = Button(root, text="STOP", width=8, height=2, 
                   bg="#D9290B", fg="black",
                   font=('URW Gothic L', 16, 'bold'),
                   activebackground='#AE220B'
                   )
on1_btn = Button(root, text="STOP", width=8, height=2, 
                   bg="#D9290B", fg="black",
                   font=('URW Gothic L', 16, 'bold'),
                   activebackground='#AE220B'
                   )

start_btn.place(x=30,y=60)





root.mainloop()
