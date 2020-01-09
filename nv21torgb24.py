#!/usr/bin/python
# -*- coding: utf-8 -*-

# 各种YUV格式详解: https://www.jianshu.com/p/e67f79f10c65
# 1. Y∈ [0,1] U∈ [-0.5,0.5] V∈ [-0.5 ,0.5]
# 2. Y∈[16,235] U∈[16,240] V∈[ 16,240 ]
# 3. jpeg的标准中，Y、U、V的取值范围都是0-255
# NV21是420sp的一种，先V后U，YYYYYYYYVUVU
# 本文针对jpeg标准

#[Y,U,V]T =  M[R,G,B]T   其中 M = 0.299 , 0.587, 0.114, -0.169,   - 0.331,   0.5,     0.5,  - 0.419    - 0.081　　 
#[R,G,B]T =  M[Y,U,V]T  其中 M = 1    0   1.4017       1   -0.3437   -0.7142      1   1.7722   
#0YUV量化后   （Y(16,235)   U(16,240)   V( 16,240 )）　　
#[Y,U,V,1]T =  M[R,G,B,1]T 其中 M =  [ 0.2568, 0.5041, 0.0979, 16-0.1479, -0.2896, 0.4375, 1280.4375, -0.3666, -0.0709, 128, 0, 0, 0, 1 ]
#[R,G,B,1]T = M[Y,U,V,1]T            M =  1.1644   0   1.6019   -223.5521   1.1644   -0.3928   -0.8163   136.1381   1.1644   2.0253   0   -278.0291   0.0000   0.0000   0.0000   1.0000

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

            # 虽然图片的实际YUV值的范围是0-254，但是当成MPEG的量化能得到较好图片
            Y = (ord(Y) - 16) / (235.0 - 16)
            U = (ord(U) - 16) / (240.0 - 16) - 0.5
            V = (ord(V) - 16) / (240.0 - 16) - 0.5

            R = Y + 1.4017 * V;
            G = Y - 0.3437 * U - 0.7142 * V;
            B = Y + 1.7722 * U

            R = clamp2byte(R * 255)
            G = clamp2byte(G * 255)
            B = clamp2byte(B * 255)

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
