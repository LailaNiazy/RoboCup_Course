# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 15:25:20 2018

@author: looly
"""
import numpy as np
import math
import cv2
from naoqi import ALProxy
from ball_detection_fcn_center import ball_detection

ip_addr = "169.254.28.227"  # Replace here with your NaoQi's IP address.
port_num = 9559

# get NAOqi module proxy
motion = ALProxy("ALMotion", ip_addr, port_num)
posture = ALProxy("ALRobotPosture", ip_addr, port_num)
videoDevice = ALProxy('ALVideoDevice', ip_addr, port_num)

string ="images" + "/*.png"
motion.wakeUp()
fractionMaxSpeed = 0.8

 # Go to posture stand
posture.goToPosture("StandInit", fractionMaxSpeed)
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
lower= (0,8,105)
upper = (41, 255, 255)

while True:
    #untitled1.template_matching(string)
    center = ball_detection(image,videoDevice,captureDevice,height,width,lower,upper)
    
    if 135 < center[0] < 186:
        pass
    else: 
        math.sin(abs(center[0]-160))
        motion = ALProxy("ALMotion", ip_addr, 9559)
        # Set stiffness on for Head motors
        motion.setStiffnesses("Head", 1.0)
        
        # Will go to 1.0 then 0 radian
        # in two seconds
        motion.post.angleInterpolation(["HeadYaw"],
            [1.0, 0.0],
            [1  , 2],
            False
        )

