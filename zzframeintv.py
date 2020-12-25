#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, os
import shutil as sh

rawintv = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 4.0, 6.0, 8.0, 10.0]

if len(sys.argv) < 2:
    print('Usage:')
    print('    %s <xxx.csv>' % (sys.argv[0]))
    print('example:    %s 3dof_rgb_1min.csv' % (sys.argv[0]))
    sys.exit(0)

ts = []
with open(sys.argv[1]) as f:
    while True:
        line = f.readline()
        if not line:
            break
        ss = line.split(',')
        if len(ss) >= 2:
            try:
                for i in range(2):
                    ss[i] = int(ss[i])
                ts.append(ss[:2])
            except:
                continue

print('head 10 Mtime,Htime:')
for t in ts[:10]:
    print(t[0], t[1])

# intv ms -> us
for i in range(len(rawintv)):
    rawintv[i] = int(rawintv[i]*1000)
print(rawintv)

intvs = []
for i in range(1, len(ts)):
    mintv = ts[i][0] - ts[i - 1][0]
    hintv = ts[i][1] - ts[i - 1][1]
    intvs.append((mintv, hintv))
print(intvs[:10])

mspecs = {}
for a in rawintv:
    mspecs[a] = 0

hspecs = {}
for a in rawintv:
    hspecs[a] = 0

def tkey(t):
    for i in range(len(rawintv)):
        if rawintv[i] > t:
            return rawintv[i - 1]
    return rawintv[-1]

for a in intvs:
    mintv = a[0]
    hintv = a[1]
    mspecs[tkey(mintv)] = mspecs[tkey(mintv)] + 1
    hspecs[tkey(hintv)] = hspecs[tkey(hintv)] + 1

print(mspecs)
print(hspecs)

total = len(intvs)
print('MTime:')
for i in range(len(rawintv)):
    print('[%.1fms - %.1fms]' % (rawintv[i]/1000.0, rawintv[i+1]/1000.0 if i != len(rawintv) - 1 else 9999999), '%.2f%%' % (mspecs[rawintv[i]] * 100.0 / total))
#print('MTime average: %.1fms' % ())
print('')
print('HTime:')
for i in range(len(rawintv)):
    print('[%.1fms - %.1fms]' % (rawintv[i]/1000.0, rawintv[i+1]/1000.0 if i != len(rawintv) - 1 else 9999999), '%.2f%%' % (hspecs[rawintv[i]] * 100.0 / total))
