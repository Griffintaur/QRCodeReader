# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 21:56:30 2017

@author: 310247467
"""

class PatternFinding(object):
    
    def __init__(self,contours_group,image):
        self.image2=image
        if contours is None:
            print "Please provide contours"
        else:
            thresholdImage, contours, hierarchy=contours_group
            self.Contours=contours
            self.ThresholdImage=thresholdImage
            self.Hierarchy=hierarchy
            
    def CheckContourWithinContourHavingLevel(self,nooflevels):
        """This function checks whether there is contour inside another contour till level as mentioned in the nooflevels"""
        for contour,index in enumerate(self.Contours):
            IsPattern=self.IsPossibleQRContour(index)
            if IsPattern is True:
                x,y,w,h=cv.boundingRect(self.Contours[index])
                cv.rectangle(self.image2,(x,y),(x+w,y+h),(0,255,0),2)
                cv.imshow("hello",self.image2)
            cv.waitKey(0)
            
        
    def CheckingRatioOfContours(self,index):
        """This Functions checks whether contours are in the certain ratio or not.This is required for qr as the qr has the contours in the specific ratio"""
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
        level=0
        while tempContourChild !=-1:
            level=level+1
            tempContourChild=self.Hierarchy[0,tempContourChild,3]
        if(level>=6):
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
     