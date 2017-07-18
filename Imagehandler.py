# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 14:28:26 2017

@author: Ankit Singh
"""
import cv2 as cv
import os.path
import numpy as np

class Imagehandler(object):
    def __init__(self,path):
        if (os.path.exists(path) and os.path.isfile(path)):
            self.ImagePath=path
        else:
            print "file not found"
    
    def __convertImagetoBlackWhite(self):
        self.Image=cv.imread(self.ImagePath,cv.IMREAD_COLOR)
        self.image2=self.Image
        if(self.Image is None):
            print "some problem with the image"
        else:
            print "Image Loaded"
            
        self.Image=cv.cvtColor(self.Image,cv.COLOR_BGR2GRAY)
        self.Image=cv.adaptiveThreshold(self.Image,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,11,2)
        return self.Image
    
    def WritingImage(self,image):
        if(image is None):
            print"Image is not valid.Please select some other image"
        else:
            nameAppended=self.ImagePath.split("/")
            image=cv.cvtColor(self.Image,cv.COLOR_BGR2GRAY)
            cv.imwrite('qrcode'+nameAppended[len(nameAppended)-1],image)
            cv.imshow('qrcode'+nameAppended[len(nameAppended)-1],image)
            cv.waitKey(0);
        
    def GetImageContour(self):
        thresholdImage= self.__convertImagetoBlackWhite()
        thresholdImage=cv.Canny(thresholdImage,100,200)
        thresholdImage, contours, hierarchy = cv.findContours(thresholdImage,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        #uncomment this to see the contours on the image
        #cv2.drawContours(thresholdImage, contours, -1, (0,255,0), 3)
        self.Hierarchy=hierarchy
        self.Contours=contours
        areas= [cv.contourArea(contour) for contour in contours]
        for index in xrange(len(contours)):
            IsPattern=self.IsPossibleQRContour(index)
            if IsPattern is True:
                x,y,w,h=cv.boundingRect(contours[index])
                cv.rectangle(self.image2,(x,y),(x+w,y+h),(0,0,255),2)
                cv.imshow("hello",self.image2)
        maxAreaIndex=np.argmax(areas)
        x,y,w,h=cv.boundingRect(contours[maxAreaIndex])
        cv.rectangle(self.image2,(x,y),(x+w,y+h),(0,255,0),2)
        cv.imshow("hello",self.image2)
        cv.waitKey(0)
        contour_group=(thresholdImage, contours, hierarchy)
        return contour_group
    
    def __isContourInsideContour(self,contourindexa,contourindexb,heir):
        index=contourindexa
        while heir[0,index,3] != contourindexb:
            t=heir[0,index,3]
            if t==-1:
                return False
            index=t
        return False
    def ComputeRatioOfAreasofContourInside(self,index):
        firstchildindex=self.Hierarchy[0,index,3]
        secondchildindex=self.Hierarchy[0,firstchildindex,3]
        areaoffirst=cv.contourArea(self.Contours[index])/cv.contourArea(self.Contours[firstchildindex])
        areaofsecondchild=cv.contourArea(self.Contours[firstchildindex])/cv.contourArea(self.Contours[secondchildindex])
        
        print areaoffirst
        print areaofsecondchild
        if areaofsecondchild >0.8 and areaofsecondchild< 1:
            return True
        else:
            return False

    
        
        
    def IsPossibleQRContour(self,contourindex):
        """since contours belonging to QR have 6 other contours inside it.It is because every border is counted as contour in the Opencv"""
        tempContourChild=self.Hierarchy[0,contourindex,3]
        #print tempContourChild
        level=0
        while tempContourChild !=-1:
            level=level+1
            tempContourChild=self.Hierarchy[0,tempContourChild,3]
        if(level==3):
            print level
            IsAreaSame=self.ComputeRatioOfAreasofContourInside(contourindex)
            if IsAreaSame is True:
                return True
            else:
                return False
            return True
        else:
            return False

    def __compareContourArea(self,contourindexa,contourindexb,contours):
        if(cv.contourArea(contours[contourindexa]) >cv.contourArea(contours[contourindexb])):
            return True
        else:
            return False
    def LimitContourNumbers(self,minPix,maxPix,contours):
        contours=[contours.remove(contour) for contour in contours if (cv.contourArea(contour)<minPix or cv.contourArea(contour)>maxPix)]
        return contours
        
    def reduceImageContour(self):
        contours=self.GetImageContour()
        
        
        
    
