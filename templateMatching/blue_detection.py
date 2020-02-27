# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 16:30:32 2018

@author: looly
"""

# vim: set fileencoding=utf-8 :
from collections import deque
#import sys
import imutils
import numpy as np
import cv2
from naoqi import ALProxy
import template_matching


#upper = (180, 255, 255)
#lower = (150, 150, 0)
#lower= (105,8,0)
#upper = (255, 255, 41)
def blue_detection(image,videoDevice,captureDevice,height,width,lower,upper,detector,startX, startY, endX, endY):

    bodyshape=cv2.imread("temp2.png")
    
    bodyshape = cv2.cvtColor(bodyshape, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(bodyshape, 127, 255, 0)
    contour_mask, contour_body, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour_body=contour_body[1]
    
#    torso_template=cv2.imread("template_torso.jpg")
#    w_torso, h_torso,_ = torso_template.shape[::-1]
#    torso_template=cv2.cvtColor(torso_template,cv2.COLOR_BGR2GRAY)                
#    torso_template=cv2.Canny(torso_template,50, 200)
#    torso_template=cv2.resize(torso_template, (70, 70))                
                    
    
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
         
            # construct a mask for the color "blue", then perform
            # a series of dilations and erosions to remove any small
            # blobs left in the mask
        mask = cv2.inRange(blurred, lower, upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        res = cv2.bitwise_and(image,image, mask= mask)
############################crop blue area#############################################        
#        image_grey=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY);
#        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        # only proceed if at least one contour was found
        
#        if len(cnts) > 0:
#                # find the largest contour in the mask, then use
#                # it to compute the minimum enclosing circle and
#                # centroid
#                c = max(cnts, key=cv2.contourArea)
#                x,y,w,h = cv2.boundingRect(c)
#                crop_image = image_grey[y-50:y+h+50, x-50:x+w+50]
#                crop_image = image[y-50:y+h+50, x-50:x+w+50]
         
#                height, width, _ = image.shape

#####################################advanced template matching################################              
                #crop_image=template_matching.template_matching(image,videoDevice,captureDevice,width,height)                
                
###################################failed tempalte matching########################################
#                height, width, _ = crop_image.shape
#                crop_image=cv2.cvtColor(crop_image,cv2.COLOR_BGR2GRAY)                
#                crop_image=cv2.Canny(crop_image,50, 200)
#                
#                
#                result = cv2.matchTemplate(crop_image, torso_template, cv2.TM_CCOEFF)
#                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
#                top_left = max_loc
#                bottom_right = (top_left[0] + w_torso, top_left[1] + h_torso)
#
###########################failed shape comaprison replaced by template matching###########################
#                cv2.rectangle(image,top_left, bottom_right, 255, 2)
#                min_x, min_y = width, height
#                max_x = max_y = 0
#                ret, thresh = cv2.threshold(crop_image, 127, 255, 0)
#                contour_image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#                if len(contours) != 0:
#                    ret=[]
#                    #for i in contours:
#                    ret=cv2.matchShapes(i,contour_body,1,0.0)
#                        
#                    if ret <=1:
#                        #for indx,i in enumerate(contours):
#                           # if ret[indx]==min(ret):
#                        (x,y,w,h) = cv2.boundingRect(contours)
#                        min_x, max_x = min(x, min_x), max(x+w, max_x)
#                        min_y, max_y = min(y, min_y), max(y+h, max_y)
#                        if w > 80 and h > 80:
#                            cv2.rectangle(image, (x,y), (x+w,y+h), (0, 0, 255), 2)
#                                
#                        if max_x - min_x > 0 and max_y - min_y > 0:
#                            cv2.rectangle(image, (min_x, min_y), (max_x, max_y), (0, 0, 255), 2)
         
                #cv2.imshow("top-camera-320x240", image)
        cv2.imshow('mask', mask)
        #cv2.imshow('res',res)
        #cv2.imshow("troso",torso_template)
        #cv2.imshow('crop',crop_image)
        
        keypoints = detector.detect(mask)
        
        counter = 0
        for key in keypoints:
            if startX < key.pt[0] < endX and startY < key.pt[1] < endY:
               counter+= 1
        
        if counter != 0:
            return True
        else:
            return False