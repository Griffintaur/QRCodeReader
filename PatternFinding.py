# -*- coding: utf-8 -*-
"""
Created on  Jul 16 21:56:30 2017

@author: Ankit Singh
"""
import cv2 as cv
class PatternFinding(object):
    
    def __init__(self,contours_group,image):
        self.image=image
        if contours_group is None:
            print "Please provide contours"
        else:
            thresholdImage, contours, hierarchy=contours_group
            self.Contours=contours
            self.ThresholdImage=thresholdImage
            self.Hierarchy=hierarchy
            
    def CheckContourWithinContourHavingLevel(self,nooflevels):
        """This function checks whether there is contour inside another contour till level as mentioned in the nooflevels"""
        patterns=[]
        for index in xrange(len(self.Contours)):
            IsPattern=self.IsPossibleQRContour(index)
            if IsPattern is True:
                patterns.append(self.Contours[index])
                x,y,w,h=cv.boundingRect(self.Contours[index])
                cv.rectangle(self.image,(x,y),(x+w,y+h),(0,255,0),2)
                cv.imshow("hello",self.image)    
        cv.waitKey(0)
        return patterns
            
        
    def CheckingRatioOfContours(self,index):
        """This Functions checks whether contours are in the certain ratio or not.This is required for qr as the qr has the contours in the specific ratio"""
        firstchildindex=self.Hierarchy[0,index,3]
        secondchildindex=self.Hierarchy[0,firstchildindex,3]
        areaoffirst=cv.contourArea(self.Contours[index])/cv.contourArea(self.Contours[firstchildindex])
        areaofsecondchild=cv.contourArea(self.Contours[firstchildindex])/cv.contourArea(self.Contours[secondchildindex])
        
        print areaoffirst
        print areaofsecondchild
        print (areaoffirst/areaofsecondchild)
        if (areaoffirst/areaofsecondchild)> 1 and (areaoffirst/areaofsecondchild)< 10:
            return True
        else:
            return False    
    def FindingPatterns(self):
        pass
        
    def __isContourBInsideContourA(self,contourindexa,contourindexb,heir):
        index=contourindexa
        while heir[0,index,3] != contourindexb:
            t=heir[0,index,3]
            if t==-1:
                return False
            index=t
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
            IsAreaSame=self.CheckingRatioOfContours(contourindex)
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
     