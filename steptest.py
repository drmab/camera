from gpiozero import OutputDevice
from signal import pause

btn = Button(21)

# motor
IN1 = OutputDevice(6)
IN2 = OutputDevice(13)
IN3 = OutputDevice(19)
IN4 = OutputDevice(26)
stepPins = [IN1,IN2,IN3,IN4]
seq = [[1,0,0,0],
       [0,1,0,0],
       [0,0,1,0],
       [0,0,0,1]]
stepCounter = 0

def stepOne():
  for pin in range(0,4):
    xPin=stepPins[pin]          # Get GPIO
    if seq[stepCounter][pin]!=0:
      xPin.on()
    else:
      xPin.off()
  stepCounter += 1
  if (stepCounter >= 4):
    stepCounter = 0

btn.when_pressed = stepOne

pause()

