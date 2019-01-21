# -*- coding: utf-8 -*-
"""
Created on  Jul 16 21:05:31 2016

@author: AnkitSingh
"""
import cv2 as cv
import numpy as np
from FindingOrientationOfContours import Quad


class AffineTransformation(object):

    def __init__(self, image, orientation):
        if image is None:
            print('Unable to read the Image. Please provide the image file')
        else:
            self.OriginalImage = image
        self.TransformImage = None
        self.ORIENTATION = orientation

    def transform(self, PointTop, PointRight, PointBottom):
        Point1 = [PointTop[0], PointTop[1]]
        Point2 = [PointRight[0], PointRight[1]]
        Point3 = [PointBottom[0], PointBottom[1]]
        src = np.float32([Point1, Point2, Point3])
        dest_pointTop = [40, 40]
        dest_pointRight = [140, 40]
        dest_pointBottom = [40, 140]
        destination = np.float32(
            [dest_pointTop, dest_pointRight, dest_pointBottom])
        affineTrans = cv.getAffineTransform(src, destination)
        self.TransformImage = cv.warpAffine(
            self.OriginalImage, affineTrans, self.OriginalImage.shape[:2])
        self.TransformImage = self.TransformImage[0:200, 0:200]
        # cv.imshow("TransformImage",self.TransformImage)            #uncomment to debug
        # cv.waitKey(0)
        # cv.destroyAllWindows()
        return self.TransformImage


class PerspectiveTransformation(object):
    def __init__(self, image, orientation):
        if image is None:
            print('Unable to read the Image. Please provide the image file')
        else:
            self.OriginalImage = image
        self.TransformImage = None
        self.ORIENTATION = orientation

    def determineLocation(self, messQuad=None):
        TopQuad = self.findConers(messQuad.TopContour)
        RightQuad = self.findConers(messQuad.RightContour)
        BottomQuad = self.findConers(messQuad.BottomContour)
        self.wholeQuad = self.determineWholeQuad(TopQuad, RightQuad, BottomQuad)
        return self.wholeQuad

    def transform(self, messQuad):
        self.determineLocation(messQuad)
        src = np.float32([self.wholeQuad.tl, self.wholeQuad.tr, self.wholeQuad.br, self.wholeQuad.bl])
        print(src)
        dst = np.float32([[0, 0], [200, 0], [200, 200], [0, 200]])
        warpMatrix = cv.getPerspectiveTransform(src, dst)
        self.TransformImage = cv.warpPerspective(self.OriginalImage, warpMatrix, (200, 200))
        return self.TransformImage

    # To find the bottom right point of the QR code
    def __findBr(self, RightQuad, BottomQuad):
        print(self.ORIENTATION)
        if self.ORIENTATION == "NorthWest":
            return self.getIntersectionPoint(RightQuad.tr, RightQuad.br, BottomQuad.br, BottomQuad.bl)
        elif self.ORIENTATION == "SouthEast":
            return self.getIntersectionPoint(RightQuad.tl, RightQuad.bl, BottomQuad.tl, BottomQuad.tr)
        elif self.ORIENTATION == "SouthWest":
            return self.getIntersectionPoint(RightQuad.tl, RightQuad.tr, BottomQuad.tr, BottomQuad.br)
        elif self.ORIENTATION == "NorthEast":
            return self.getIntersectionPoint(RightQuad.br, RightQuad.bl, BottomQuad.tl, BottomQuad.bl)

    # To determine the absolute position of the four points in QR code
    def determineWholeQuad(self, TopQuad, RightQuad, BottomQuad):
        bottomRight = self.__findBr(RightQuad, BottomQuad)
        if self.ORIENTATION == "NorthWest":
            return Quad(TopQuad.tl, RightQuad.tr, bottomRight, BottomQuad.bl)
        elif self.ORIENTATION == "SouthEast":
            return Quad(TopQuad.br, RightQuad.bl, bottomRight, BottomQuad.tr)
        elif self.ORIENTATION == "SouthWest":
            return Quad(TopQuad.bl, RightQuad.tl, bottomRight, BottomQuad.br)
        elif self.ORIENTATION == "NorthEast":
            return Quad(TopQuad.tr, RightQuad.br, bottomRight, BottomQuad.tl)

    # Point a1 and a2 in the line1 ,b1 b2 in the line2 ,get the intersection of these two lines
    def getIntersectionPoint(self, a1, a2, b1, b2):
        r = a2 - a1
        s = b2 - b1
        t = b1 - a1
        ratio = np.cross(t, s) / np.cross(r, s)
        target = ratio * r + a1
        return target

    # To figure out the relative position (Relative to the whole picture) of the angular point in a contour
    def findConers(self, contour):
        peri = cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, 0.02 * peri, True)
        if len(approx) == 4:
            approx = approx.reshape(4, 2)
            # self.drawConers(approx)
            # cv.imshow("test",self.OriginalImage)
            # cv.waitKey(0)
        else:
            # I have no idea when it unequal to 4
            pass
        quad = Quad()

        tempSum = approx.sum(axis=1)
        quad.tl = approx[np.argmin(tempSum)]
        quad.br = approx[np.argmax(tempSum)]

        tempDiff = np.diff(approx, axis=1)
        quad.tr = approx[np.argmin(tempDiff)]
        quad.bl = approx[np.argmax(tempDiff)]

        return quad

    def drawConers(self, poly):
        for point in poly:
            cv.circle(self.OriginalImage, tuple(point), 2, (0, 0, 255), -1, 8, 0)
