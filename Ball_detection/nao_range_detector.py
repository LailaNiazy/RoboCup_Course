# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 11:49:23 2018

@author: looly
"""

import cv2
#import argparse
from operator import xor
from naoqi import ALProxy
import numpy as np
from collections import deque
#import sys
#import imutils
import numpy as np
import cv2
from naoqi import ALProxy



def callback(value):
    pass


def setup_trackbars(range_filter):
    cv2.namedWindow("Trackbars", 0)

    for i in ["MIN", "MAX"]:
        v = 0 if i == "MIN" else 255

        for j in range_filter:
            cv2.createTrackbar("%s_%s" % (j, i), "Trackbars", v, 255, callback)

def get_trackbar_values(range_filter):
    values = []

    for i in ["MIN", "MAX"]:
        for j in range_filter:
            v = cv2.getTrackbarPos("%s_%s" % (j, i), "Trackbars")
            values.append(v)

    return values


def main():
    ip_addr = "169.254.28.227"  # Replace here with your NaoQi's IP address.
    port_num = 9559
    
    range_filter = 'RGB'
    # get NAOqi module proxy
    videoDevice = ALProxy('ALVideoDevice', ip_addr, port_num)
    
    # subscribe top camera
    AL_kTopCamera = 0
    AL_kQVGA = 1            # 320x240
    AL_kBGRColorSpace = 13
    captureDevice = videoDevice.subscribeCamera(
        "test", AL_kTopCamera, AL_kQVGA, AL_kBGRColorSpace, 10)
    
    # create image
    width = 320
    height = 240
    image = np.zeros((height, width, 3), np.uint8)

    setup_trackbars(range_filter)
    
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
                    
    
        if range_filter == 'RGB':
            frame_to_thresh = image.copy()
        else:
            frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values(range_filter)
    
        thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))
    
        
        cv2.imshow("Original", image)
        cv2.imshow("Thresh", thresh)
    
        if cv2.waitKey(1) & 0xFF is ord('q'):
            break


if __name__ == '__main__':
    main()