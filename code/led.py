import os
import RPi.GPIO as GPIO
import time
import threading

os.system('clear')

led1 = 23
led2 = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def startSystem():
    GPIO.output(led1, True)
    GPIO.output(led2, False)
    timesleep(10)
    GPIO.output(led1, False)
    GPIO.output(led2, True)
    timesleep(10)
    

        


