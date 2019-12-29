from gpiozero import LED, Button, OutputDevice
from picamera import PiCamera
from datetime import datetime
from signal import pause
from time import sleep

# Motor
IN1 = OutputDevice(6)
IN2 = OutputDevice(13)
IN3 = OutputDevice(19)
IN4 = OutputDevice(26)
stepPins = [IN1,IN2,IN3,IN4] # Motor GPIO pins</p><p>
stepDir = 1

seq = [[1,0,0,0], # Define step sequence as shown in manufacturers datasheet
             [0,1,0,0],
             [0,0,1,0],
             [0,0,0,1]]
#stepCount = 4
waitTime = 0.004    # 2 miliseconds was the maximun speed got on my tests
#stepCounter = 0

Button.was_held = False

btn = Button(21)
led = LED(12)
camera = PiCamera()
camera.start_preview()

def stepone():
  for stepCounter in range(0,3):
    for pin in range(0,4):
      xPin=stepPins[pin]          # Get GPIO
      if seq[stepCounter][pin]!=0:
        xPin.on()
      else:
        xPin.off()
    sleep(0.004) 

def capture():
    led.on()
    timestamp = datetime.now().isoformat()
    camera.capture('/home/pi/pictures/%s.jpg' % timestamp)
    led.off()

def record():
    led.on()
    timestamp = datetime.now().isoformat()
    camera.start_recording('/home/pi/videos/%s.h264' % timestamp)
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
