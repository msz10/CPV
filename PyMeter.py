# CS 6475 Computational Photography Spring 2016
# PyMeter: An approach to find distance of an object from the camera
# Author: S.Z.
# Credit: T.R. - blog.tibarazmi.com
# python PyMeter.py

import numpy as np
import cv2
import optparse

def marker_finder(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 35, 125)

    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnt = max(cnts, key = cv2.contourArea)

    return cv2.minAreaRect(cnt)

def PyMeter(knownWidth, focalLength, perWidth):
	return (knownWidth * focalLength) / perWidth

opter = optparse.OptionParser()
opts, args = opter.parse_args()

if len(args) == 0:
    opter.error("Width and Path to image expected, got %d , e.g. PyMeter.py 12 photo.jpg" % len(args))

elif len(args) == 2:
    WIDTH = args[0]
    PATH = args[1]
else:
    opter.error("Width and Path to image expected, got %d" % len(args))

KNOWN_DISTANCE = 1.6
conW= float(WIDTH)
KNOWN_WIDTH = conW

print "Known Width (Letter paper): " , KNOWN_WIDTH
conP= str(PATH)
IMG_PATH = [conP]
print "Image Path: " , IMG_PATH

img = cv2.imread(IMG_PATH[0])
marker = marker_finder(img)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
print "Focal Length: ", focalLength /10

for imgP in IMG_PATH:
	img = cv2.imread(imgP)
	marker = marker_finder(img)
	inches = PyMeter(KNOWN_WIDTH, focalLength, marker[1][0])

	drawBox = np.int0(cv2.cv.BoxPoints(marker))
	cv2.drawContours(img, [drawBox], -1, (0, 255, 0), 2)
	cv2.putText(img, "Distance %.2fft" % (focalLength / 10), (img.shape[1] - 350, img.shape[0] - 355), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 230), 3)

	cv2.imshow("image", img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	