import picamera
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

picno = 0
cameraPin = 23      # make sure the input wires (to the buttons) don't cross
videoPin = 24
ledPin = 25     # any values from 330 ohm up to 1000 ohm are fine
GPIO.setup(cameraPin, GPIO.IN)
GPIO.setup(videoPin, GPIO.IN)
GPIO.setup(ledPin, GPIO.OUT)
camera = picamera.PiCamera()

alreadyPressed = False
videoOn = False

while True:
    cameraPressed = GPIO.input(cameraPin)
    videoPressed = GPIO.input(videoPin)

    if not cameraPressed and not alreadyPressed and not videoOn:
        GPIO.output(ledPin, 1)          # maybe GPIO.HIGH / GPIO.LOW
        camera.resolution = (2560, 1920)
        camera.capture("image{}.jpg".format(picno))
        GPIO.output(ledPin, 0)
        picno = picno + 1

    elif not videoPressed:
        if videoOn:
            camera.stop_recording()
            GPIO.output(ledPin, 0)
            videoOn = False
        else:
            GPIO.output(ledPin, 1)
            camera.resolution = (1920, 1080)      # may want to change that
            camera.start_recording("image{}.h264".format(picno))
            videoOn = True
            picno = picno + 1

    alreadyPressed = cameraPressed
    sleep(0.5)
