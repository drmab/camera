from gpiozero import LED, Button
from picamera import PiCamera
from datetime import datetime
from signal import pause

cameraButton = Button(21)
videoButton = Button(20)
led = LED(12)
camera = PiCamera()
camera.start_preview()

def capture():
    led.on()
    timestamp = datetime.now().isoformat()
    camera.capture('/home/pi/%s.jpg' % timestamp)
    led.off()

def record():
    led.on()
    timestamp = datetime.now().isoformat()
    camera.start_recording('/home/pi/%s.h264' % timestamp)
    videoButton.wait_for_release()
    camera.stop_recording()
    led.off()

cameraButton.when_pressed = capture
videoButton.when_pressed = record

pause()
