import time
from gpiozero import OutputDevice
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
stepCount = 4
waitTime = 0.004    # 2 miliseconds was the maximun speed got on my tests
stepCounter = 0

while (stepCounter < stepCount):
  for pin in range(0,4):
    xPin=stepPins[pin]          # Get GPIO
    if seq[stepCounter][pin]!=0:
      xPin.on()
    else:
      xPin.off()
  stepCounter += stepDir
  time.sleep(waitTime)     # Wait before moving on
