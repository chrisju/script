#!/usr/bin/python
# -*- coding: utf-8 -*-

# 各种YUV格式详解: https://www.jianshu.com/p/e67f79f10c65
# 1. Y∈ [0,1] U∈ [-0.5,0.5] V∈ [-0.5 ,0.5]
# 2. Y∈[16,235] U∈[16,240] V∈[ 16,240 ]
# 3. jpeg的标准中，Y、U、V的取值范围都是0-255
# NV21是420sp的一种，先V后U，YYYYYYYYVUVU
# 本文针对jpeg标准

import sys
import os

def clamp2byte(v):
    if v < 0:
        return chr(0)
    elif v > 255:
        return chr(255)
    else:
        return chr(int(v))

def convert(src, width, height):
    dst = ''
    for y in range(height):
        for x in range(width):
            Y = src[y * width + x]
            V = src[width * height + (y / 2) * width + (x / 2) * 2]
            U = src[width * height + (y / 2) * width + (x / 2) * 2 + 1]

            Y = ord(Y)
            U = ord(U)
            V = ord(V)

            R = Y + 1.402 * (V - 128);
            G = Y - 0.34413 * (U - 128) - 0.71414 * (V - 128);
            B = Y + 1.772 * (U - 128)

            R = clamp2byte(R)
            G = clamp2byte(G)
            B = clamp2byte(B)

            dst += R
            dst += G
            dst += B
    return dst

if __name__ == '__main__':

    path = sys.argv[1]
    width = int(sys.argv[2])

    src = None
    with open(path, 'rb') as f:
        src = f.read()
        print(src[:100])

    height = int(len(src)/1.5/width)
    print('height:' , height)

    dst = convert(src, width, height)

    with open(path + '.dst', 'wb') as f:
        f.write(dst)
