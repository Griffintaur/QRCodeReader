# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 22:39:34 2017

@author: 310247467
"""

from Imagehandler import Imagehandler

if __name__ == "__main__":
    directorypath="C:\Users\\310247467\Desktop\learn\qr\\"
    images=['qr1.png', 'qr2.png', 'qr3.jpg', 'qr4.jpg']
    paths=[directorypath+ image for image in images]
    obj=Imagehandler(paths[0])
    obj.GetImageContour()
