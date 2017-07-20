# -*- coding: utf-8 -*-
"""
Created on  Jun 16 22:39:34 2016

@author: AnkitSingh
"""

from Imagehandler import Imagehandler
import yaml
import glob
import os

def App():
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    IOPlaces=cfg['Main']
    input=IOPlaces['Input']
    output=IOPlaces['Output']
    directorypath=input
    os.chdir(input)
    filesTypes=cfg['FileType']
    images=[]
    for filetype in filesTypes:
        images.extend(glob.glob("*."+filetype))
    paths=[directorypath+image for image in images]
    for i in xrange(len(paths)):
        obj=Imagehandler(paths[i])
        TransformImage=obj.QRCodeInImage()
        if TransformImage is  None:
            print "Image is not generated"
        obj.WritingImage(TransformImage,str(output),'output'+str(i)+'.jpg')
    


if __name__ == "__main__":
     App()
