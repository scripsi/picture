#!/usr/bin/env python

from gpiozero import LED
from smbus import SMBus
from bme280 import BME280
from picamera2 import Picamera2
from libcamera import Transform
from time import sleep
import datetime
from uptime import boottime
import cv2 as cv
import numpy as np
import smtplib
import ssl
import mimetypes
from email.message import EmailMessage
from configparser import ConfigParser

ini = ConfigParser()
ini.read("/home/pi/picture.ini")

led1 = LED(23)
led2 = LED(24)
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)
bme280.setup(mode="forced")
print(bme280.get_temperature())
print(bme280.get_humidity())

# Capture image
led1.on()
led2.on()
camera=Picamera2()
camera_config=camera.create_still_configuration(transform=Transform(hflip=True, vflip=True),
                                                controls={"ExposureTime": 4000000})
camera.configure(camera_config)
camera.start() 

sleep(1)
img=camera.capture_array()
sleep(1)
camera.close()
led1.off()
led2.off()

# process image
#cv.imwrite("/home/pi/picture/image.jpg",img)

# Image slice coordinates are [start_y:end_y, start_x:end_x]
meter_a_img = img[740:790,550:750]
meter_b_img = img[1170:1230,1460:1660]

# create datestamps and filename
date_img=np.zeros((20,200,3),np.uint8)
date_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
email_date_text = datetime.datetime.now().strftime('%A, %d %B %Y at %H:%M')
img_file_name=datetime.datetime.now().strftime('%Y%m%d-%H%M') + "-meter.jpg"
cv.putText(date_img,date_text,(5,15),cv.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1,2)

# create uptime info
boot_text = 'Running since ' + boottime().strftime('%H:%M:%S on %A, %d %B %Y')

# create weather info
temperature = bme280.get_temperature()
humidity = bme280.get_humidity()
weather_text='Temperature: {:.1f}C\nHumidity: {:.1f}%'.format(temperature,humidity)
all_meter_img = cv.vconcat([meter_a_img,meter_b_img,date_img])
#cv.imwrite("/home/pi/picture/meter.jpg",all_meter_img)

# convert image to bytes
ret,jpg=cv.imencode(".jpg",all_meter_img)
binary_data = jpg.tobytes()

# create email message
msg = EmailMessage()
msg['Subject'] = 'South Cottage Electricity Meter Readings'
msg['From'] = ini['default']['fromaddress']
msg['To'] = ini['default']['toaddress']
# Set text content
msg.set_content("South Cottage meter readings taken on "
                + email_date_text
                + "\n\nSee attached picture:\n\n  Heating Rate Meter\n  Standard Rate Meter (ignore rightmost digit)\n  Time of Reading\n\n"
                + weather_text + "\n"
                + boot_text + "\n")

# attach picture
msg.add_attachment(binary_data, maintype='image', subtype='jpeg', filename=img_file_name)

# Send email
# context = ssl.create_default_context()

# with smtplib.SMTP_SSL(ini['default']['server'], 465, context=context) as server:
with smtplib.SMTP(ini['default']['server']) as server:
    server.login(ini['default']['user'], ini['default']['password'])
    server.send_message(msg)
    
