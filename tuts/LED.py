import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23,GPIO.OUT)
print "LED on"
GPIO.output(23,GPIO.HIGH)
time.sleep(5)
print "LED off"
GPIO.output(23,GPIO.LOW)
GPIO.setup(24,GPIO.OUT)
print "LED on"
GPIO.output(24,GPIO.HIGH)
time.sleep(5)
print "LED off"
GPIO.output(24,GPIO.LOW)
