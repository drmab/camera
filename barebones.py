# Barebone camera script
# see:
# https://github.com/adafruit/adafruit-pi-cam/blob/master/cam.py

import atexit
import io
import os
import os.path
import fnmatch
import picamera
import pygame
import stat
import time
import yuv2rgb
from pygame.locals import *
from gpiozero import Button

# Global stuff -------------------------------------------------------------

pathData = '/home/pi/Photos'
sizeData = [(2592, 1944), (320, 240), (0.0   , 0.0   , 1.0   , 1.0   )]
saveIdx = 0
screenMode = 3
# find the right one
button = Button(17)

# Assorted utility functions -----------------------------------------------

def imgRange(path):
	min = 9999
	max = 0
	try:
	  for file in os.listdir(path):
	    if fnmatch.fnmatch(file, 'IMG_[0-9][0-9][0-9][0-9].JPG'):
	      i = int(file[4:8])
	      if(i < min): min = i
	      if(i > max): max = i
	finally:
	  return None if min > max else (min, max)

def takePicture():
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
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

# Init camera and set up default values
camera            = picamera.PiCamera()
atexit.register(camera.close)
camera.resolution = sizeData[1]
camera.crop       = (0.0, 0.0, 1.0, 1.0)


# Main loop ----------------------------------------------------------------

while True:
    if button.is_pressed:
      print("Pressed")
      takePicture()
    else:
      # print("Not pressed")
      # Refresh display
      stream = io.BytesIO() # Capture into in-memory stream
      camera.capture(stream, use_video_port=True, format='raw')
      stream.seek(0)
      stream.readinto(yuv)  # stream -> YUV buffer
      stream.close()
      yuv2rgb.convert(yuv, rgb, sizeData[1][0],sizeData[1][1])
      img = pygame.image.frombuffer(rgb[0:
      (sizeData[1][0] * sizeData[1][1] * 3)],
      sizeData[1], 'RGB')

      if img:
	screen.blit(img,
	((320 - img.get_width() ) / 2,
	(240 - img.get_height()) / 2))
      pygame.display.update()

    sleep(2)
