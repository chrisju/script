#!/usr/bin/env python2
# coding = utf8

import sys
import os

n = 10
ipfile = '/home/zz/bin/DNS'
tmpfile = '/tmp/mpinglog'

def out():
    f = open(tmpfile)
    for line in f.readlines():
        if line.strip() and not line.startswith('#'):
            if line.startswith('---') \
                    or line.startswith('rtt') \
                    or line.find('packets transmitted') != -1:
                        print line,

if __name__ == '__main__':
    print 'start ping for ' + str(n) + ' times...'

    if len(sys.argv) > 1:
        ipfile = sys.argv[1]
    f = open(ipfile)
    for line in f.readlines():
        if line.strip() and not line.startswith('#'):
            cmd = 'ping -c ' + str(n) + ' ' + line[:-1] \
                    + ' > ' + tmpfile
#            print cmd
            os.system(cmd)
            out()


