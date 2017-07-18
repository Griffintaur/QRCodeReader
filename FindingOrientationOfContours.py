# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 20:56:17 2017

@author: Ankit Singh
"""
class FindingOrientationOfContours(object):
     def FindOrientation(contourA,contourB,ContourC):
         """Here famous Triangle Method is used to determine the Orientation of the three contours
         and identify which one is top, left and right contour.Here we find the distance betweeen the centres of mass of these three countours 
         and which ever is longest , base of the triangle formed by three contours and then we find the position of remaining contour using this base line to kno
         the orientation"""
         ##calculating the centre of mass of three contours
         MomentA=cv.moments(contourA)
         MomentB=cv.moments(conoturB)
         MomentC=cv.moments(contourC)
         ##finding the centre of mass of three contours
         centreOfMassA_X = int(MomentA['m10']/MomentA['m00'])
         centreOfMassA_Y  = int(MomentA['m01']/MomentA['m00'])
         pointA=(centreOfMassA_X,centreOfMassA_Y)
         
         centreOfMassB_X = int(MomentB['m10']/MomentB['m00'])
         centreOfMassB_Y  = int(MomentB['m01']/MomentB['m00'])
         pointB=(centreOfMassB_X,centreOfMassB_Y)
         
         centreOfMassC_X = int(MomentC['m10']/MomentC['m00'])
         centreOfMassC_Y  = int(MomentC['m01']/MomentC['m00'])
         pointC=(centreOfMassC_X,centreOfMassC_Y)
         
         ###finding the distance of the distance between points
         distance_AB=self.__findDistanceBetweenTwoPoints(PointA,PointB)
         distance_BC=self.__findDistanceBetweenTwoPoints(PointB,PointC)
         distance_AC=self.__findDistanceBetweenTwoPoints(PointA,PointC)
    
         largestLine=np.argmax(np.array([distance_AB,distance_BC,distance_AC])) 
         if largestLine==0:
             #largest line is between points A and B
             Right,Bottom,Top=findOrientation(pointC,PointA,pointB)
         
         if largestLine==1:
             #LargestLine is Between B and C
             Right,Bottom,Top=findOrientation(pointA,PointB,pointC)
         if largestLine==2:
             #LargestLine is between A and C
             Right,Bottom,Top= findOrientation(pointB,PointA,pointC)
         
         
     def __findDistanceBetweenTwoPoints(PointA, PointB):
         return np.sqrt(np.square(PointA[0]-PointB[0])+np.square(PointA[1]-PointB[1]))
    
     def findOrientationBetwwenPoints(DistancePoint,SlopePointA,SlopePointB):
        Right,Bottom,Top
        slope,distance=CalculatePerpendicularDistance(DistancePoint,SlopePointA,SlopePointB)
        if slope>0 and distance>0:
            #if slope and distance are positive A is bottom while B is right
            Right=SlopePointB
            Bottom=SlopePointA
            Top=DistancePoint
        
        if slope>0 and distance<0:
            #if slope is positive and distance is negative then B is bottom while A is right
            Right=SlopePointA
            Bottom=SlopePointB
            Top=DistancePoint
            
        if slope <0 and distance >0:
            Right=SlopePointB
            Bottom=SlopePointA
            Top=DistancePoint
            
        if slope <0 and distance >0:
            Right=SlopePointA
            Bottom=SlopePointB
            Top=DistancePoint
        
        return (Right,Bottom,Top)
            
    
     def CalculatePerpendicularDistance(DistancePoint,SlopePointA,SlopePointB):
        coeffA,coeffB,constant=self.__findCoefficientsOftheLine(SlopePointA,SlopePointB)
        slope=self.__findSlope(SlopePointA,SlopePointB)
        return (slope,coeffA*DistancePoint[0]+coeffB*DistancePoint[1]+constant/(np.sqrt(coeffA**2+coeffB**2)))
    
    
     def __findCoefficientsOftheLine(pointA,pointB):
        slope=self.__findSlope(pointA, pointB)
        coefficientA=-slope
        coefficientB=1
        constant=slope*pointA[0]-pointA[1]
        return (coefficientA,coefficientA,constant)
        
    
     def __findSlope(pointA, pointB):
        return (pointB[1]-pointA[1])/(pointB[0]-pointA[0])
    