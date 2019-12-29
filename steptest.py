from gpiozero import OutputDevice
from signal import pause

Button.was_held = False

btn = Button(21)

# motor
IN1 = OutputDevice(31)
IN2 = OutputDevice(33)
IN3 = OutputDevice(35)
IN4 = OutputDevice(37)
stepPins = [IN1,IN2,IN3,IN4]
seq = [[1,0,0,0],
       [0,1,0,0],
       [0,0,1,0],
       [0,0,0,1]]
stepCounter = 0


def held(btn):
    btn.was_held = True

def released(btn):
    if not btn.was_held:
        stepOne()
    btn.was_held = False


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

btn.when_held = held
btn.when_released = released

pause()

