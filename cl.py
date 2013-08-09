#!/usr/bin/python
# -*- coding: utf-8 -*-
# linecount.py
# 2009-1-20
# author:
#    Jason Lee
# modified by zz
#
import sys
import os

exts = ['.cpp','.c','.h','.py','.java']
def read_line_count(fname):
    count = 0
    for file_line in open(fname).xreadlines():
        if len(file_line.strip()) > 0:
            count += 1
    return count

if __name__ == '__main__':

    count = 0
    fcount = 0
    path = ''
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = os.getcwd()

    for root,dirs,files in os.walk(path):
        for f in files:
            ext = os.path.splitext(f)[1]
            if ext in exts:
                fname = root + '/'+ f
                fcount += 1
                c = read_line_count(fname)
                print str(c) + '\t' + fname
                count += c

    print 'file count:%d' % fcount
    print 'count:%d' % count
