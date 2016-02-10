#from cv2 import cv
import cv2
import random
import sys
import numpy as np

print cv2.__version__

DICE_SIZE = 16
BLUR_FACTOR = 5
RED_LOW_THRESHOLD = 209
MIN_PIP_AREA = 10

def resizeRect(rect, sizeFactor):
    return (rect[0], (rect[1][0] + sizeFactor,rect[1][1] + sizeFactor), rect[2])


img = cv2.imread("dice3.jpg")

#img = cv2.imread("dice-real.jpg")
#img = cv2.imread("dice-real-2.jpg")

### Threshold image

blurred = cv2.medianBlur(img,BLUR_FACTOR)

blue = cv2.split(blurred)[0]
green = cv2.split(blurred)[1]
red = cv2.split(blurred)[2]

cv2.waitKey(0)
cv2.destroyAllWindows()