from picamera2 import Picamera2
from libcamera import Transform
from time import sleep
from pprint import *

camera=Picamera2()
camera_config=camera.create_still_configuration()
camera.configure(camera_config)
camera.start()

camera.capture_file("/home/pi/picture/image.jpg")
camera.stop()
#camera.still_configuration.size = (2592, 1944)
#camera.still_configuration.transform=Transform(hflip=1, vflip=1)
#camera_config=camera.create_still_configuration(transform=Transform(hflip=True, vflip=True))
#camera.configure(camera_config)
#camera.start() 
#sleep(1)
#camera.capture('/home/pi/picture/image.jpg')
#sleep(1)
#camera.close()
