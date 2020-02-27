# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 13:50:39 2018

@author: looly
"""

# vim: set fileencoding=utf-8 :
from collections import deque
#import sys
import imutils
import numpy as np
import cv2
from naoqi import ALProxy



#upper = (180, 255, 255)
#lower = (150, 150, 0)
#lower= (105,8,0)
#upper = (255, 255, 41)
lower= (0,8,105)
upper = (41, 255, 255)
pts = deque(maxlen=64)


ip_addr = "169.254.77.44"  # Replace here with your NaoQi's IP address.
port_num = 9559

# get NAOqi module proxy
videoDevice = ALProxy('ALVideoDevice', ip_addr, port_num)

# subscribe top camera
AL_kBottomCamera = 1
AL_kQVGA = 1            # 320x240
AL_kBGRColorSpace = 13
captureDevice = videoDevice.subscribeCamera(
    "test", AL_kBottomCamera, AL_kQVGA, AL_kBGRColorSpace, 10)

# create image
width = 320
height = 240
image = np.zeros((height, width, 3), np.uint8)

while True:

    # get image
    result = videoDevice.getImageRemote(captureDevice);

    if result == None:
        print 'cannot capture.'
    elif result[6] == None:
        print 'no image data string.'
    else:

        # translate value to mat
        values = map(ord, list(result[6]))
        i = 0
        for y in range(0, height):
            for x in range(0, width):
                image.itemset((y, x, 0), values[i + 0])
                image.itemset((y, x, 1), values[i + 1])
                image.itemset((y, x, 2), values[i + 2])
                i += 3
        #rgb to bgr for opencv 
      #  image1 = image[...,::-1]   
        blurred = cv2.GaussianBlur(image, (11, 11), 0)
        #hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
         
        	# construct a mask for the color "green", then perform
        	# a series of dilations and erosions to remove any small
        	# blobs left in the mask
        mask = cv2.inRange(blurred, lower, upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        res = cv2.bitwise_and(image,image, mask= mask)
        # find contours in the mask and initialize the current
        	# (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        		cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        center = None
         
        	# only proceed if at least one contour was found
        if len(cnts) > 0:
        		# find the largest contour in the mask, then use
        		# it to compute the minimum enclosing circle and
        		# centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            print(radius)
            # only proceed if the radius meets a minimum size
            if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(image, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(image, center, 5, (0, 0, 255), -1)
        	# update the points queue
        pts.appendleft(center)
        
        	# loop over the set of tracked points
        for i in range(1, len(pts)):
        		# if either of the tracked points are None, ignore
        		# them
        		if pts[i - 1] is None or pts[i] is None:
        			continue
         
        		# otherwise, compute the thickness of the line and
        		# draw the connecting lines
              # 64 for buffer
        		thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
        		cv2.line(image, pts[i - 1], pts[i], (0, 0, 255), thickness)
        
        cv2.imshow("top-camera-320x240", image)
        cv2.imshow('mask', mask)
        cv2.imshow('res',res)
    # exit by [ESC]
    if cv2.waitKey(33) == 27:
        break