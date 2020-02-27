#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 19:26:28 2018

@author: robocup17
"""
#from collections import deque
#import sys
#import imutils
import numpy as np
import cv2
from naoqi import ALProxy
import template_matching
import blue_detection 
ip_addr = "169.254.28.227 "  # Replace here with your NaoQi's IP address.
port_num = 9559

# get NAOqi module proxy
motion = ALProxy("ALMotion", ip_addr, port_num)
posture = ALProxy("ALRobotPosture", ip_addr, port_num)
videoDevice = ALProxy('ALVideoDevice', ip_addr, port_num)

#string ="images" + "/*.png"
#motion.wakeUp()
#fractionMaxSpeed = 0.8

 # Go to posture stand
#posture.goToPosture("StandInit", fractionMaxSpeed)
# subscribe top camera
AL_kBottomCamera = 0
AL_kQVGA = 1            # 320x240
AL_kBGRColorSpace = 13
captureDevice = videoDevice.subscribeCamera(
    "test", AL_kBottomCamera, AL_kQVGA, AL_kBGRColorSpace, 5)
# create image
width = 320
height = 240
image = np.zeros((height, width, 3), np.uint8)

lower= (58,24,0)
upper = (255, 255, 47)

params = cv2.SimpleBlobDetector_Params()
params.minThreshold = 10;
params.maxThreshold = 200;
params.filterByColor = True
params.blobColor = 255
# Filter by Area.
params.filterByArea = False
 
# Filter by Circularity
params.filterByCircularity = False
 
# Filter by Convexity
params.filterByConvexity = False
 
# Filter by Inertia
params.filterByInertia = False
 
detector=cv2.SimpleBlobDetector_create(params)

while True:
    startX, startY, endX, endY = template_matching.template_matching(image,videoDevice,captureDevice,height,width)
    flag=blue_detection.blue_detection(image,videoDevice,captureDevice,height,width,lower,upper,detector,startX, startY, endX, endY)
    
    if flag :
        cv2.rectangle(image, (startX, startY), (endX, endY), (255, 0, 0), 2)   
    
    cv2.imshow("full detection",image)
    if cv2.waitKey(33) == 27:
        break