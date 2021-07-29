#!/usr/bin/env python

from gpiozero import LED
import picamera
from time import sleep
from fractions import Fraction
import datetime
import cv2 as cv
import numpy as np

led1 = LED(23)
led2 = LED(24)

# Capture image
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
sleep(1)
camera.capture('/home/pi/picture/image.jpg')
sleep(1)
camera.close()
led1.off()
led2.off()

# process image
img=cv.imread("/home/pi/picture/image.jpg")

# Image slice coordinates are [start_y:end_y, start_x:end_x]
date_img = img[20:50, 1151:1441]
meter_a_img = img[730:780,525:815]
meter_b_img = img[1160:1200,1455:1745]
all_meter_img = cv.vconcat([date_img,meter_a_img,meter_b_img])
cv.imwrite("/home/pi/picture/meter.jpg",all_meter_img)
