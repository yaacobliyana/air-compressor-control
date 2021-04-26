from tkinter import *
import sys
import time 
import threading

#Read Pressure Sensor 1




#Start the Program for first sequence
def start1():
	if pressure1 > 45:
		print('open valve 1 & 2')
		print('close valve 3 & 4')
	else if pressure1 < 25:
		print('Close all valves')
	else:
		start1()

#Start the Program for second sequence
def start2():
	if pressure2 > 45:
		print('open valve 3 & 4')
		print('close valve 1 & 2')
	else if pressure2 < 25:
		print('Close all valves')
	else:
		start2()


