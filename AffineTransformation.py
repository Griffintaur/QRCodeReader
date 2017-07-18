# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 21:05:31 2017

@author: AnkitSingh
"""
import cv2 as cv

class AffineTransformation(object):
    
    def __init__(self,image):
        if(image is None):
            print"Unable to read the Image. Please provide the image file"
        else:
            self.OriginalImage=image
        self.TransformImage=None
    
    def Transform(self,PointTop,PointRight,PointBottom):
        src=(PointTop,PointRight,PointBottom)
        dest_pointTop=(20,20)
        dest_pointRight=(120,20)
        dest_pointBottom=(20,120)
        destination=(dest_pointTop,dest_pointRight,dest_pointBottom)
        affineTrans=cv.getAffineTransform(src,destination)
        self.TransformImage=cv.warpAffine(self.OriginalImage,affineTrans,self.OriginalImage.shape[:2])
        return self.TransformImage