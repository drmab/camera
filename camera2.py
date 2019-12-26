from gpiozero import Button
from picamera import PiCamera
from datetime import datetime
from signal import pause

cameraButton = Button(3)
videoButton = Button(4)
camera = PiCamera()
camera.start_preview()

def capture():
    timestamp = datetime.now().isoformat()
    camera.capture('/home/pi/%s.jpg' % timestamp)

def record():
    timestamp = datetime.now().isoformat()
    camera.start_recording('/home/pi/%s.h264' % timestamp)

def stopVideo():
    camera.stop_recording()

cameraButton.when_pressed = capture
videoButton.when_pressed = record
videoButton.when_released = stopVideo

pause()