from picamera import PiCamera
from time import sleep
from fractions import Fraction

camera = PiCamera(
    resolution=(1280, 720),
    framerate=Fraction(1, 6),
    sensor_mode=3)
camera.shutter_speed = 6000000
camera.iso = 800

camera.exposure_mode = 'off'
camera.start_preview()
sleep(30)
camera.capture('/home/pi/picture/image.jpg')
camera.stop_preview()
