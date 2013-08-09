#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import getopt

def usage():
    print 'change txt linesep'
    print 'usage:'
    print sys.argv[0]+' [-w|-n|-h] FILES\t'
    print '-w\tto dos linesep(default)'
    print '-n\tto *nix linesep'
    print '-h\tshow help'

if __name__ == '__main__':

    toxnix = 0
    fnames = []

    if len(sys.argv) == 1:
        usage()
        sys.exit(0)

    try:
        opts,args = getopt.getopt(sys.argv[1:], "nwh")
        fnames = args[:]
        for opt,args in opts:
            if opt == '-n':
                toxnix = 1
            elif opt == '-w':
                toxnix = 0
            elif opt == '-h':
                usage()
                sys.exit(0)
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for fname in fnames:
        f = open(fname,'r')
        f2 = open(fname+'_linesep','w')
        lines = f.xreadlines()
        for line in lines:
            if toxnix:
                line = line.replace('\r\n','\n')
            else:
                line = line.replace('\n','\r\n')
            f2.write(line)
        f.close()
        f2.close()
        os.remove(fname)
        os.rename(fname+'_linesep',fname)
