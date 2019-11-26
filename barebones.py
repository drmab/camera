# Barebone camera script
# see:
# http://learn.adafruit.com/adafruit-pitft-28-inch-resistive-touchscreen-display-raspberry-pi

import errno
import io
import os
import os.path
import picamera
import pygame
import stat
from pygame.locals import *
from gpiozero import Button

# Global stuff -------------------------------------------------------------

pathData = '/home/pi/Photos'
sizeData = [(2592, 1944), (320, 240), (0.0   , 0.0   , 1.0   , 1.0   )]
saveIdx = 0
screenMode = 3
# find the right one
button = Button(2)

# Assorted utility functions -----------------------------------------------

def takePicture():
	if not os.path.isdir(pathData):
	  try:
	    os.makedirs(pathData)
	    # Set new directory ownership to pi user, mode to 755
	    os.chown(pathData, uid, gid)
	    os.chmod(pathData,
	      stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
	      stat.S_IRGRP | stat.S_IXGRP |
	      stat.S_IROTH | stat.S_IXOTH)
	  except OSError as e:
	    # errno = 2 if can't create folder
	    print errno.errorcode[e.errno]
	    return

	# scan for the max image index, start at next pos.
	r = imgRange(pathData)
	if r is None:
	  saveIdx = 1
	else:
	  saveIdx = r[1] + 1
	  if saveIdx > 9999: saveIdx = 0


	# Scan for next available image slot
	while True:
	  filename = pathData + '/IMG_' + '%04d' % saveIdx + '.JPG'
	  if not os.path.isfile(filename): break
	  saveIdx += 1
	  if saveIdx > 9999: saveIdx = 0

	scaled = None
	camera.resolution = sizeData[0]
	camera.crop       = sizeData[2]
	try:
	  camera.capture(filename, use_video_port=False, format='jpeg',
	    thumbnail=None)
	  # Set image file ownership to pi user, mode to 644
	  # os.chown(filename, uid, gid) # Not working, why?
	  os.chmod(filename,
	    stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
	  img    = pygame.image.load(filename)
	  scaled = pygame.transform.scale(img, sizeData[1])

	finally:
	  # Add error handling/indicator (disk full, etc.)
	  camera.resolution = sizeData[1]
	  camera.crop       = (0.0, 0.0, 1.0, 1.0)


# Initialization -----------------------------------------------------------

# Init framebuffer/touchscreen environment variables
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV'      , '/dev/fb1')

# Get user & group IDs for file & folder creation
# (Want these to be 'pi' or other user, not root)
s = os.getenv("SUDO_UID")
uid = int(s) if s else os.getuid()
s = os.getenv("SUDO_GID")
gid = int(s) if s else os.getgid()

# Buffers for viewfinder data
rgb = bytearray(320 * 240 * 3)
yuv = bytearray(320 * 240 * 3 / 2)

# Init pygame and screen
pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

# Init camera and set up default values
camera            = picamera.PiCamera()
atexit.register(camera.close)
camera.resolution = sizeData[1]
camera.crop       = (0.0, 0.0, 1.0, 1.0)


# Main loop ----------------------------------------------------------------

while(True):

  # Process touchscreen input
  while True:
    if button.is_pressed:
      takePicture()
    else:
	  # Refresh display
	  stream = io.BytesIO() # Capture into in-memory stream
	  camera.capture(stream, use_video_port=True, format='raw')
	  stream.seek(0)
	  stream.readinto(yuv)  # stream -> YUV buffer
	  stream.close()
	  yuv2rgb.convert(yuv, rgb, sizeData[sizeMode][1][0],
	  sizeData[sizeMode][1][1])
	  img = pygame.image.frombuffer(rgb[0:
	  (sizeData[sizeMode][1][0] * sizeData[sizeMode][1][1] * 3)],
	  sizeData[sizeMode][1], 'RGB')
	  elif screenMode < 2: # Playback mode or delete confirmation
	  img = scaled       # Show last-loaded image
	  else:                # 'No Photos' mode
	  img = None         # You get nothing, good day sir

	  if img is None or img.get_height() < 240: # Letterbox, clear background
	  screen.fill(0)
	  if img:
		  screen.blit(img,
		  ((320 - img.get_width() ) / 2,
		  (240 - img.get_height()) / 2))
    sleep(1)
