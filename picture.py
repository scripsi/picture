#!/usr/bin/env python

from gpiozero import LED
from smbus2 import SMBus
from bme280 import BME280
from picamera2 import Picamera2
from libcamera import Transform
from time import sleep
from time import time as time_now
import datetime
from uptime import boottime
import cv2 as cv
import numpy as np
import smtplib
import ssl
import mimetypes
from email.message import EmailMessage
from configparser import ConfigParser

# *** Initialisation ***

# read ini file
ini = ConfigParser()
ini.read("/home/pi/picture.ini")

billdate = ini['default']['billdate']
# If billing date, take pictures of whole meter, otherwise just the display
if datetime.date.today().day == billdate:
  BILLDAY = True
  CAMERA_CONTROLS = {"ExposureTime": 1000000, "AnalogueGain":2.0}
  img_start_x = 1000
  img_end_x = 1570
  img_start_y = 630
  img_end_y = 1430
  img_width = 570
else:
  BILLDAY = False
  CAMERA_CONTROLS = {"ExposureTime": 1000000, "AnalogueGain":4.0}
  img_start_x = 1200
  img_end_x = 1400
  img_start_y = 1000
  img_end_y = 1070
  img_width = 200

meter_img = []

capture_interval = 7
camera=Picamera2()
camera_config=camera.create_still_configuration(transform=Transform(hflip=True, vflip=True),
                                                controls=CAMERA_CONTROLS})
camera.configure(camera_config)

led1 = LED(23)
led2 = LED(24)
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)
bme280.setup(mode="forced")

# *** Capture images ***
led1.on()
led2.on()

camera.start() 

sleep(1)

for i in range(4):
  begin_capture = time_now()
  img = camera.capture_array()
  # Image slice coordinates are [start_y:end_y, start_x:end_x]
  meter_img.append(img[img_start_y:img_end_y,img_start_x:img_end_x])
  while time_now() < (begin_capture + capture_interval):
    sleep(1)

camera.close()
led1.off()
led2.off()

# *** Email images ***

# create datestamps and filename
date_img=np.zeros((20,img_width,3),np.uint8)
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
all_meter_img = cv.vconcat([meter_img[0],meter_img[1],meter_img[2],meter_img[3],date_img])
#cv.imwrite("/home/pi/picture/meter.jpg",all_meter_img)

# convert image to bytes
cv.IMWRITE_JPEG_QUALITY = 70
ret,jpg=cv.imencode(".jpg",all_meter_img)
binary_data = jpg.tobytes()

# create email message
msg = EmailMessage()
msg['Subject'] = 'South Cottage Electricity Meter Reading'
msg['From'] = ini['default']['fromaddress']
msg['To'] = ini['default']['toaddress']
# Set text content
msg.set_content("South Cottage meter reading taken on "
                + email_date_text
                + "\n\nUse kWh reading from attached picture.\n\n"
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
    
