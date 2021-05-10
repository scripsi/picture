from gpiozero import LED
from picamera import PiCamera
from time import sleep
from fractions import Fraction

led1 = LED(23)
led2 = LED(24)
led1.on()
led2.on()
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
led1.off()
led2.off()
