#!/usr/bin/python
#  --*-- coding:utf-8  --*--

from PIL import Image
import os
import sys


if len(sys.argv) != 4:
    print "Usage:\n\tpython %s source_type target_type dir" % sys.argv[0]
    sys.exit()

arg="."+sys.argv[1].lower()
arg1="."+sys.argv[2].lower()

#********************* 当前目录下指定格式的图像文件名 ***********************
def getImageFiles():
    allfiles = os.listdir(sys.argv[3])

    files = []

    for f in allfiles:
        if f[-4:].lower()==arg:
            files.append(f)

    return files

#********************* 转换 **************************************************
def CovImage():

    filename=getImageFiles()
    for i in filename:
        x=i[:-4]
        Image.open(i).save(x+arg1)



if __name__ == "__main__":

    CovImage()
