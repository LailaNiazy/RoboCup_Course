#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 19:04:22 2018

@author: robocup17
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 19:04:31 2018

@author: looly
"""

# import the necessary packages
import numpy as np
import argparse
import imutils
import glob
import cv2
 
# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-t", "--template", required=True, help="Path to template image")
#ap.add_argument("-i", "--images", required=True,
#    help="Path to images where template will be matched")
#ap.add_argument("-v", "--visualize",
#    help="Flag indicating whether or not to visualize each iteration")
#args = vars(ap.parse_args())
def template_matching(image,videoDevice,captureDevice,height,width):
# load the image image, convert it to grayscale, and detect edges
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
        template = cv2.imread('template.jpg')
        template=cv2.resize(template,(30,30))
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template = cv2.Canny(template, 50, 200)
        (tH, tW) = template.shape[:2]
        visualize=False
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        found = None
            # loop over the scales of the image
        for scale in np.linspace(0.2, 1.0, 20)[::-1]:
                # resize the image according to the scale, and keep track
                # of the ratio of the resizing
                resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
                r = gray.shape[1] / float(resized.shape[1])
         
                # if the resized image is smaller than the template, then break
                # from the loop
                if resized.shape[0] < tH or resized.shape[1] < tW:
                    break
        
                # detect edges in the resized, grayscale image and apply template
                # matching to find the template in the image
                edged = cv2.Canny(resized, 50, 200)
                result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
                (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
         
                # check to see if the iteration should be visualized
                if visualize:
                    # draw a bounding box around the detected region
                    clone = np.dstack([edged, edged, edged])
                    cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
                        (maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
                    cv2.imshow("Visualize", clone)
                    cv2.waitKey(0)
         
                # if we have found a new maximum correlation value, then ipdate
                # the bookkeeping variable
                if found is None or maxVal > found[0]:
                    found = (maxVal, maxLoc, r)
                    
            # unpack the bookkeeping varaible and compute the (x, y) coordinates
            # of the bounding box based on the resized ratio
        (_, maxLoc, r) = found
        (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
        (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
         
            # draw a bounding box around the detected result and display the image
        image_copy=image.copy() 
        cv2.rectangle(image_copy, (startX, startY), (endX, endY), (0, 0, 255), 2)
        cv2.imshow("detection",image_copy)
        return startX, startY, endX, endY