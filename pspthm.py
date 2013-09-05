#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
生成psp视频缩略图
'''

import sys
import os

for f in os.listdir('.'):
    ss= os.path.splitext(f)
    if ss[1].lower() == '.mp4':
        cmd = ('ffmpeg -i "%s.mp4" -f image2 -ss 12 -vframes 10 '
                '-s 160x120 -an "%s.thm" > /dev/null') % (ss[0],ss[0])
        print(cmd)
        os.system(cmd)

