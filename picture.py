from gpiozero import LED
import picamera
from time import sleep
from fractions import Fraction
import datetime

led1 = LED(23)
led2 = LED(24)
led1.on()
led2.on()
camera = picamera.PiCamera(
    resolution=(2592, 1944),
    framerate=Fraction(1, 6),
    sensor_mode=3)
camera.shutter_speed = 4000000
camera.iso = 800
camera.rotation = 180
camera.exposure_mode = 'off'
camera.annotate_background = picamera.Color('black')
camera.annotate_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# camera.start_preview()
# sleep(20)
sleep(1)
camera.capture('/home/pi/picture/image.jpg')
# camera.stop_preview()
sleep(1)
camera.close()
led1.off()
led2.off()
