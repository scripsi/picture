import cv2 as cv
import numpy as np

#img=cv.imread("image.jpg",cv.IMREAD_GRAYSCALE)
img=cv.imread("image.jpg")
#ret,oimg = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
#gimg = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)
date_img = img[20:50, 1151:1441]
meter_a_img = img[730:780,525:815]
meter_b_img = img[1160:1200,1455:1745]
cv.imwrite("datestamp.png",date_img)
cv.imwrite("heating-meter.png",meter_a_img)
cv.imwrite("standard-meter.png",meter_b_img)
all_img = cv.vconcat([date_img,meter_a_img,meter_b_img])
cv.imwrite("all-meter.jpg",all_img)
