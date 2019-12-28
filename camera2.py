from gpiozero import LED, Button
from picamera import PiCamera
from datetime import datetime
from signal import pause

Button.was_held = False

btn = Button(21)
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

def held(btn):
    btn.was_held = True
    record()

def released(btn):
    if not btn.was_held:
        capture()
    btn.was_held = False

btn.when_held = held
btn.when_released = released

pause()

