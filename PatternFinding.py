# -*- coding: utf-8 -*-
"""
Created on  Jul 16 21:56:30 2016

@author: Ankit Singh
"""
import cv2 as cv
import numpy as np


class PatternFinding(object):
    def __init__(self, contours_group, image):
        self.image = image
        if not contours_group:
            print ('Please provide contours')
        else:
            thresholdImage, contours, hierarchy = contours_group
            self.Contours = contours
            self.ThresholdImage = thresholdImage
            self.Hierarchy = hierarchy

    def CheckContourWithinContourHavingLevel(self, nooflevels):
        """This function checks whether there is contour inside another
        contour till level as mentioned in the nooflevels"""
        patterns = []
        patterns_indices = []
        for index in range(len(self.Contours)):
            IsPattern = self.IsPossibleQRContour(index, nooflevels)
            if IsPattern is True:
                patterns.append(self.Contours[index])
                # print self.Contours[index]
                patterns_indices.append(index)
                # patterns_dictionary[hash(tuple(self.Contours[index]))]=index
        #cv.waitKey(0)
        return patterns, patterns_indices

    def FindingQRPatterns(self, nooflevels):
        """This function filters to have only three QR patterns"""
        patterns, patterns_dictionary = \
            self.CheckContourWithinContourHavingLevel(nooflevels)  #returns contours and list of indices
                                                                   #of the returned contours
        QRPatterns = []

        while len(patterns) < 3:
            nooflevels = nooflevels-1
            patterns, patterns_dictionary = \
                self.CheckContourWithinContourHavingLevel(nooflevels)

        if len(patterns) == 3:
            print ('patterns are less than equal to three')
            for ind in range(len(patterns)):
                x, y, w, h = cv.boundingRect(patterns[ind])
                cv.rectangle(
                    self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                #cv.imshow('qr box found', self.image)              #uncomment to debug
                #cv.waitKey(0)
                #cv.destroyAllWindows()
            return patterns
        else:
            area_patterns = np.array(
                [cv.contourArea(pattern) for pattern in patterns])
            arg_areapatterns = np.argsort(area_patterns)
            passage_dictinary = {}
            for i in range(len(patterns)):                 #pick the largest area contour
                index = patterns_dictionary[arg_areapatterns[
                    len(arg_areapatterns) - i - 1]]
                if not index:
                    print ('contour not found in the dictionary')
                else:
                    # print 'papa is', self.Hierarchy[0][index][3]
                    if self.Hierarchy[0][index][3] == -1:
                        passage_dictinary[index] = -1
                    else:
                        if self.IsparentAlreadyThere(passage_dictinary, index):
                            passage_dictinary[index] = 1
                            # print 'got one',self.Hierarchy[0][index][3]
                        else:
                            passage_dictinary[index] = -1

        for ind in range(len(patterns)):
            mapping = patterns_dictionary[ind]
            if passage_dictinary[mapping] == -1:
                x, y, w, h = cv.boundingRect(self.Contours[mapping])
                cv.rectangle(
                    self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                #cv.imshow('contour of qr', self.image)         #uncomment to debug
                #cv.waitKey(0)
                QRPatterns.append(patterns[ind])
                #cv.destroyAllWindows()
        if len(QRPatterns) > 3:
            QRPatterns_new = []
            area_patterns = np.array([
                cv.contourArea(QRpattern) for QRpattern in QRPatterns])
            arg_areapatterns = np.argsort(area_patterns)
            for i in range(3):                     #pick the best three
                QRPatterns_new.append(QRPatterns[arg_areapatterns[
                    len(arg_areapatterns) - i - 1]])
                x, y, w, h = cv.boundingRect(QRPatterns_new[i])
                cv.rectangle(
                    self.image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                #cv.imshow('best qr contour', self.image)           #uncomment to debug
                #cv.waitKey(0)
                #cv.destroyAllWindows()
            QRPatterns = QRPatterns_new
        return QRPatterns

    def IsparentAlreadyThere(self, passage_dictinary, index): #Checks if Parent exists which is present in
        parent = self.Hierarchy[0][index][3]                  #passage_dictionary
        while (parent != -1) and (parent not in passage_dictinary.keys()):
            parent = self.Hierarchy[0][parent][3]

        return not (parent == -1)

    def CheckingRatioOfContours(self, index):
        """This Functions checks whether contours are in the certain ratio
        or not.This is required for qr as the qr has the contours in the
        specific ratio"""
        firstchildindex = self.Hierarchy[0][index][2]
        secondchildindex = self.Hierarchy[0][firstchildindex][2]
        areaoffirst = cv.contourArea(self.Contours[index]) / (
            cv.contourArea(self.Contours[firstchildindex]) + 1e-5)
        areaofsecondchild = cv.contourArea(self.Contours[firstchildindex]) / (
            cv.contourArea(self.Contours[secondchildindex]) + 1e-5)

        # x,y,w,h=cv.boundingRect(self.Contours[firstchildindex])
        # cv.rectangle(self.image,(x,y),(x+w,y+h),(0,0,255),2)
        # x,y,w,h=cv.boundingRect(self.Contours[index])
        # cv.rectangle(self.image,(x,y),(x+w,y+h),(0,0,255),2)
        # x,y,w,h=cv.boundingRect(self.Contours[secondchildindex])
        # cv.rectangle(self.image,(x,y),(x+w,y+h),(0,0,255),2)
        # print areaoffirst
        # print areaofsecondchild
        # print (areaoffirst/areaofsecondchild)

        return ((areaoffirst / areaofsecondchild) > 1 and \
           ((areaoffirst / areaofsecondchild) < 10))


    def FindingPatterns(self):
        pass

    def __isContourBInsideContourA(self, contourindexa, contourindexb, heir):
        index = contourindexa
        while heir[0, index, 3] != contourindexb:
            t = heir[0, index, 3]
            if t == -1:
                return False
            index = t
        return False

    def IsPossibleQRContour(self, contourindex, nooflevels):
        """since contours belonging to QR have 6 other contours
        inside it.It is because every border is counted as
        contour in the Opencv"""
        tempContourChild = self.Hierarchy[0][contourindex][2]
        # print tempContourChild
        level = 0
        while tempContourChild != -1:
            level = level+1
            tempContourChild = self.Hierarchy[0][tempContourChild][2]

        if (level >= nooflevels):
            #print level
            IsAreaSame = self.CheckingRatioOfContours(contourindex)
            return (IsAreaSame is True)
        else:
            return False

    def __compareContourArea(self, contourindexa, contourindexb, contours):
        if cv.contourArea(contours[contourindexa]) > \
           cv.contourArea(contours[contourindexb]):
            return True
        else:
            return False

    def LimitContourNumbers(self, minPix, maxPix, contours):
        contours = [contours.remove(contour) for contour in contours if
                    ((cv.contourArea(contour) < minPix) or
                     (cv.contourArea(contour) > maxPix))]

        return contours

    def reduceImageContour(self):
        # contours = self.GetImageContour()
        self.GetImageContour()
