#Ugly as shit wall of text code that works. Still trying to re write it to be not so shit, but it works.
#Adapted from github user "andli" https://github.com/andli/dicecounter

import cv2
import numpy as np
print cv2.__version__
DICE_SIZE = 16
BLUR_FACTOR = 5
RED_LOW_THRESHOLD = 209
MIN_PIP_AREA = 10
loopCount = 0
def resizeRect(rect, sizeFactor):
	return (rect[0], (rect[1][0] + sizeFactor,rect[1][1] + sizeFactor), rect[2])
img = cv2.imread("dice2.png")
blurred = cv2.medianBlur(img,BLUR_FACTOR)
blue = cv2.split(blurred)[0]
green = cv2.split(blurred)[1]
red = cv2.split(blurred)[2]
diceblocks = cv2.threshold(red, RED_LOW_THRESHOLD, 255, 1)
invdiceblocks = 255 - diceblocks[1]
pyramids = cv2.distanceTransform(invdiceblocks, 2, 3)
cv2.normalize(pyramids, pyramids, 0, 1.2, cv2.NORM_MINMAX)
markers = cv2.threshold(pyramids, 0.8, 1, 0)[1]
bwImg = cv2.convertScaleAbs(markers * 255)
_, pyramids, hierarchy = cv2.findContours(bwImg.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
print str(len(pyramids)) + " dice."
for pyramid in pyramids:
	rect = cv2.minAreaRect(pyramid)
	rect = resizeRect(rect, DICE_SIZE)
	floatBox = cv2.boxPoints(rect)
	intBox = np.int0(floatBox)
	bwImg = cv2.drawContours(bwImg,[intBox],0,(255,0,0),-1)
	pts1 = floatBox
	a,b,c,d = cv2.boundingRect(intBox)
	pts2 = np.float32([[a,b],[a+c,b],[a,b+d],[a+c,b+d]])
	M = cv2.getPerspectiveTransform(pts1,pts2)
	dst = cv2.warpPerspective(bwImg,M,pts2.shape)
_, contours, hierarchy = cv2.findContours(bwImg.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
pips = 255 - cv2.threshold(cv2.cvtColor(blurred, cv2.COLOR_RGB2GRAY), 200, 255, 1)[1]
onlypips = cv2.bitwise_and(bwImg,pips)
dice = cv2.cvtColor(onlypips, cv2.COLOR_GRAY2RGB)
dice_results = [0,0,0,0,0]
wrongdice = 0
for contour in contours:
	pips = 0
	rect = cv2.minAreaRect(contour)
	floatBox = cv2.boxPoints(rect)
	intBox = np.int0(floatBox)
	a,b,c,d = cv2.boundingRect(intBox)
	subimage = onlypips[b:b+d,a:a+c]
	_,pip_contours, subhierarchy = cv2.findContours(subimage.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	for pip in pip_contours:
		if cv2.contourArea(pip) >= MIN_PIP_AREA:
			pips = pips + 1
	if pips > 6 or pips == 0:
		wrongdice = wrongdice + 1
		print pips
	else:
		dice_results[loopCount] = pips
		cv2.putText(dice,str(pips),(a,b-5),0,1,(0,0,255))
		loopCount += 1
dice_results.sort()
print dice_results
print str(wrongdice) + " erroneous objects found."
cv2.drawContours(dice,contours,-1,(255,255,0),1)
cv2.imshow('Dice', dice)
cv2.imshow('Original',img)
def doCallbackTest(value):
	tmpImg = red.copy()
	newImg = 255 - cv2.threshold(tmpImg, value, 255, 1)[1] #cv2.threshold(src, thresh, maxval, type
	cv2.imshow('Dice',newImg)
lowThreshold = 1
max_lowThreshold = 255
cv2.waitKey(0)
cv2.destroyAllWindows()