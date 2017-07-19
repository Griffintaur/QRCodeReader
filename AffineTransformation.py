# -*- coding: utf-8 -*-
"""
Created on  Jul 16 21:05:31 2017

@author: AnkitSingh
"""
import cv2 as cv
import numpy as np

class AffineTransformation(object):
    
    def __init__(self,image):
        if(image is None):
            print"Unable to read the Image. Please provide the image file"
        else:
            self.OriginalImage=image
        self.TransformImage=None
    
    def Transform(self,PointTop,PointRight,PointBottom):
        Point1=[PointTop[0],PointTop[1]]
        Point2=[PointRight[0],PointRight[1]]
        Point3=[PointBottom[0],PointBottom[1]]
        src=np.float32([Point1,Point2,Point3])
        dest_pointTop=[20,20]
        dest_pointRight=[120,20]
        dest_pointBottom=[20,120]
        destination=np.float32([dest_pointTop,dest_pointRight,dest_pointBottom])
        affineTrans=cv.getAffineTransform(src,destination)
        self.TransformImage=cv.warpAffine(self.OriginalImage,affineTrans,self.OriginalImage.shape[:2])
        cv.imshow("TransformImage",self.TransformImage)
        cv.waitKey(0)
        return self.TransformImage