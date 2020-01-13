#!/usr/bin/python
# -*- coding: utf-8 -*-

# 各种YUV格式详解: https://www.jianshu.com/p/e67f79f10c65
# 1. Y∈ [0,1] U∈ [-0.5,0.5] V∈ [-0.5 ,0.5]
# 2. Y∈[16,235] U∈[16,240] V∈[ 16,240 ]
# 3. jpeg的标准中，Y、U、V的取值范围都是0-255
# NV21是420sp的一种，先V后U，YYYYYYYYVUVU
# 本文针对jpeg标准

#[Y,U,V]T =  M[R,G,B]T   其中 M = 0.299 , 0.587, 0.114, -0.169,   - 0.331,   0.5,     0.5,  - 0.419    - 0.081　　 
#[R,G,B]T = M[Y,U,V]T 其中 M =
#1 0 1.4017
#1 -0.3437 -0.7142
#1 1.7722 0

import sys
import os
from nv21torgb24table import *

def clamp2byte(v):
    if v < 0:
        return chr(0)
    elif v > 255:
        return chr(255)
    else:
        return chr(int(v))

def clamp(v, minv, maxv):
    if v < minv:
        return minv
    elif v > maxv:
        return maxv
    else:
        return v

def convert(src, width, height, table):
    dst = ''
    p = 0
    for y in range(height):
        for x in range(width):
            Y = src[y * width + x]
            V = src[width * height + (y / 2) * width + (x / 2) * 2]
            U = src[width * height + (y / 2) * width + (x / 2) * 2 + 1]

            # 虽然图片的实际YUV值的范围是0-254，但是当成MPEG的量化能得到较好图片
            Y = clamp(ord(Y), 16, 235)
            U = clamp(ord(U), 16, 240)
            V = clamp(ord(V), 16, 240)

            index = 220 + int((U - 16) * 225 + (V - 16))
            premul = table[index]

            #R = Y + 1.4017 * V;
            #G = Y - 0.3437 * U - 0.7142 * V;
            #B = Y + 1.7722 * U
            Y = table[Y - 16]
            R = Y + premul[0]
            G = Y - premul[1]
            B = Y + premul[2]

            R = clamp2byte(R >> 16)
            G = clamp2byte(G >> 16)
            B = clamp2byte(B >> 16)

            dst += R
            dst += G
            dst += B
    return dst

def build_table():
    # 将乘法做成查表
    # 建立Y -> (Y - 16) / (235.0 - 16)
    # 建立(U,V)->((U - 16) / (240.0 - 16) - 0.5, (V - 16) / (240.0 - 16) - 0.5)->(1.4017 * V, 0.3437 * U + 0.7142 * V, 1.7722 * U)的转换表
    # 注意UV取值范围，先对齐值再用表
    # 由于是顺序无跳值，表可以转为数组
    # *255量化RGB，再乘65536，浮点转整数
    table = [0] * (220 + 225 * 225)
    for Y in range(16, 236):
        table[Y - 16] = int((Y - 16) / (235.0 - 16) * 255 * 65536)
    for U in range(16, 241):
        for V in range(16, 241):
            index = 220 + int((U - 16) * 225 + (V - 16))
            fU = (U - 16) / (240.0 - 16) - 0.5
            fV = (V - 16) / (240.0 - 16) - 0.5
            table[index] = (int(1.4017 * fV * 255 * 65536), int(0.3437 * fU * 255 * 65536 + 0.7142 * fV * 255 * 65536), int(1.7722 * fU * 255 * 65536))
    return table

if __name__ == '__main__':

    path = sys.argv[1]
    width = int(sys.argv[2])

    src = None
    with open(path, 'rb') as f:
        src = f.read()
        print(src[:100])

    height = int(len(src)/1.5/width)
    print('height:' , height)

    table = build_table()
    #with open('nv21torgb24table.py', 'w') as f:
    #    f.write('table = [');
    #    for i in range(len(table)):
    #        f.write('%s,' % repr(table[i]))
    #    f.write(']');
    with open('nv21torgb24table.h', 'w') as f:
        f.write('const int nv21torgb24_table_y[220] = {');
        for i in range(220):
            f.write('%d,' % table[i])
        f.write('};\n');
        f.write('const int nv21torgb24_table_uv[225*225][3] = {');
        for i in range(220, 220 + 225 * 225):
            f.write('{%d,%d,%d},' % table[i])
        f.write('};');

    dst = convert(src, width, height, table)

    with open(path + '.dst', 'wb') as f:
        f.write(dst)
