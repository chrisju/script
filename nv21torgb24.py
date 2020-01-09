#!/usr/bin/python
# -*- coding: utf-8 -*-

# NV21是420sp的一种，YYYYVUVUVU

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
    #dst = ['0' for i in range(width * height * 3)]
    #dst = ''.join(dst)

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
