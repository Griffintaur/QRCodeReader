# -*- coding: utf-8 -*-
"""
Created on  Jun 16 14:28:26 2016

@author: Ankit Singh
"""
import cv2 as cv
import os.path
from PatternFinding import PatternFinding
from FindingOrientationOfContours import FindingOrientationOfContours
from AffineTransformation import AffineTransformation

class Imagehandler(object):
    def __init__(self,path):
        if (os.path.exists(path) and os.path.isfile(path)):
            self.ImagePath=path
        else:
            raise OSError('Invalid path specified in `config.yml`.')

    def __convertImagetoBlackWhite(self):
        self.Image=cv.imread(self.ImagePath,cv.IMREAD_COLOR)
        self.imageOriginal=self.Image
        if(self.Image is None):
            print "some problem with the image"
        else:
            print "Image Loaded"

        self.Image=cv.cvtColor(self.Image,cv.COLOR_BGR2GRAY)
        self.Image=cv.adaptiveThreshold(self.Image,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,11,2)
        return self.Image

    def WritingImage(self,image,path,imageName):
        if(image is None):
            print"Image is not valid.Please select some other image"
        else:
            image=cv.cvtColor(image,cv.COLOR_BGR2RGB)
            print path+imageName
            cv.imwrite(path+imageName,image)
            cv.imshow(imageName,image)
            cv.waitKey(0);

    def GetImageContour(self):
        thresholdImage= self.__convertImagetoBlackWhite()
        thresholdImage=cv.Canny(thresholdImage,100,200)
        thresholdImage, contours, hierarchy = cv.findContours(thresholdImage,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        self.Contours=contours
        #uncomment this to see the contours on the image
        #cv2.drawContours(thresholdImage, contours, -1, (0,255,0), 3)
#        patternFindingObj=PatternFinding()
#        areas= [cv.contourArea(contour) for contour in contours]
#        for index in xrange(len(contours)):
#            IsPattern=self.IsPossibleQRContour(index)
#            if IsPattern is True:
#                x,y,w,h=cv.boundingRect(contours[index])
#                cv.rectangle(self.imageOriginal,(x,y),(x+w,y+h),(0,0,255),2)
#                cv.imshow("hello",self.imageOriginal)
#        maxAreaIndex=np.argmax(areas)
#        x,y,w,h=cv.boundingRect(contours[maxAreaIndex])
#        cv.rectangle(self.image2,(x,y),(x+w,y+h),(0,255,0),2)
#        cv.imshow("hello",self.imageOriginal)
#        cv.waitKey(0)
        contour_group=(thresholdImage, contours, hierarchy)
        return contour_group

    def QRCodeInImage(self):
        patternFindingObj=PatternFinding(self.GetImageContour(),self.imageOriginal)
        patterns=patternFindingObj.FindingQRPatterns(3)
        if len(patterns):
            print "patterns unble to find"
        contourA=patterns[0]
        contourB=patterns[1]
        contourC=patterns[2]
        orientationObj=FindingOrientationOfContours()
        Right,Bottom,Top=orientationObj.FindOrientation(contourA,contourB,contourC)
        print Right[0]
        print Bottom[0]
        print Top[0]
        affineTransformObj=AffineTransformation(self.imageOriginal)
        self.TransformImage=affineTransformObj.Transform(Top,Right,Bottom)
        return self.TransformImage
