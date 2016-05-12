#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, os
import shutil


if len(sys.argv) < 2:
    print 'example: %s SRR061048' % (sys.argv[0])
    print 'example: %s SRR_Acc_List.txt' % (sys.argv[0])

def getsrr(ac):
    fmt = 'ftp://ftp-trace.ncbi.nih.gov/sra/sra-instant/reads/ByRun/sra/%s/%s/%s/%s.sra'
    url = fmt % (ac[:3],ac[:6],ac,ac)
    print('downloading',url)
    #cmd = 'wget -c %s -O %s.sra' % (url,ac)
    cmd = 'axel -n 1 -s 800000 %s -o %s.sra  ' % (url,ac)
    print cmd
    os.system(cmd)


ac = sys.argv[1]
if os.path.exists(ac) and os.path.isfile(ac):
    with open(ac) as f:
        l = f.readlines()
    for name in l:
        if name.startswith('SRR'):
            getsrr(name)
elif ac.startswith('SRR'):
    getsrr(ac)
