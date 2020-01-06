import glob
import os
from random import randint
import time
import sys
import RPi.GPIO as GPIO
import picamera

camera = picamera.PiCamera()

addr = '70:2C:1F:3E:BB:F1@' # the printer's MAC address
# these are arbitrary for the moment
photoPin = 26
videoPin = 19
flashOnPin = 13
flashOffPin = 6
flashPin = 16
printPin = 18

useFlash = True

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(photoPin,GPIO.IN)
GPIO.setup(videoPin,GPIO.IN)
GPIO.setup(flashOnPin,GPIO.IN)
GPIO.setup(flashOffPin,GPIO.IN)
GPIO.setup(printPin,GPIO.IN)
# GPIO.setup(22,GPIO.OUT)
# GPIO.setup(23,GPIO.OUT)
# GPIO.setup(24,GPIO.OUT)
GPIO.setup(flashPin,GPIO.OUT)
GPIO.output(flashPin,GPIO.HIGH)

def printLastPic():
    imglist = glob.glob('/images/*.jpg')
    latest_img = max(imglist, key=os.path.getctime)

    p = subprocess.Popen(['ussp-push', addr, latest_img, 'toprint.jpg'], stdout=PIPE, stderr=PIPE)
    while p.poll() == None:
        ledtolight = randint(22, 24)
        timetolight = randint(3, 7)/10
        GPIO.output(ledtolight,GPIO.HIGH)
        time.sleep(timetolight)
        GPIO.output(ledtolight,GPIO.LOW)

    return

while True:
    if (GPIO.input(photoPin)==1):
        if (useFlash):
            GPIO.output(flashPin,GPIO.LOW)

        picName = "img_" + str(time.time()) + ".jpg"
        print("click!")
        camera.capture(picName)
        if (useFlash):
            GPIO.output(flashPin,GPIO.HIGH)
    if (GPIO.input(flashOnPin)==1):
        print("Flash On")
        useFlash = True
    if (GPIO.input(flashOffPin)==1):
        print("Flash Off")
        useFlash = False
    if (GPIO.input(printPin)):
        printLastPic
    time.sleep(0.1)
