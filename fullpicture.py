#!/usr/bin/env python

from gpiozero import LED
from picamera2 import Picamera2
from libcamera import Transform
from time import sleep
import datetime
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

email_date_text = datetime.datetime.now().strftime('%A, %d %B %Y at %H:%M')
img_file_name=datetime.datetime.now().strftime('%Y%m%d-%H%M') + "-allmeters.jpg"

# convert image to bytes
ret,jpg=cv.imencode(".jpg",img)
binary_data = jpg.tobytes()

# create email message
msg = EmailMessage()
msg['Subject'] = 'South Cottage Electricity Meter Board'
msg['From'] = ini['default']['fromaddress']
msg['To'] = ini['default']['toaddress']
# Set text content
msg.set_content("South Cottage meter board taken on "
                + email_date_text
                + "\n\nSee attached picture.\n\n")

# attach picture
msg.add_attachment(binary_data, maintype='image', subtype='jpeg', filename=img_file_name)

# Send email
context = ssl.create_default_context()

with smtplib.SMTP_SSL(ini['default']['server'], 465, context=context) as server:
    server.login(ini['default']['user'], ini['default']['password'])
    server.send_message(msg)
    
