#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019-12-26
# author: zz
#
import sys
import os
import zhconv

if __name__ == '__main__':

    os.mkdir('outputs')
    for path in sys.argv[1:]:
        with open('outputs/'+path, 'w') as fw:
            with open(path) as fr:
                fw.write(zhconv.convert(fr.read().decode('utf8'), 'zh-cn').encode('utf8'))
