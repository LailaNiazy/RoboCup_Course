#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 18:11:40 2018

@author: robocup17
"""
import cv2

bodyshape=cv2.imread("temp2.png")
    
bodyshape1 = cv2.cvtColor(bodyshape, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(bodyshape1, 200, 255, 0)
contour_mask, contour_body, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

contour_body=contour_body[1]
bodyshape=cv2.drawContours(bodyshape, contour_body, -1, (255,0,0), 10)
cv2.imshow("bodyshape1",bodyshape)
cv2.waitKey(0)