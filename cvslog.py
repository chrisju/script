#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# author: chrisju

import sys, os
import shutil as sh
import re
import getopt
import time
import shlex
import subprocess
import tempfile

#show cvs log pretty
#cvslog    #git logc
#cvslog -f   #git logfile


def usage():
    print(
'''\
usage: cvslog [-f] [-h] [--help] [PATH]
'''
    )


#l.append((fl[i],rev,date,user,change,desc))
#[[(user,desc,time),(),(),()],[(user,desc,time),(),(),()]]
def indexcommit(commits, a):
    for i in range(len(commits)):
        c = commits[i]
        if c[0][0] != a[3]:
            continue
        if c[0][1] != a[5]:
            continue
        # commit time difference low than 180s
        if abs(c[0][2] - a[2]) > 180:
            continue
        return i
    return -1

def add2commit(commits, a):
    i = indexcommit(commits, a)
    if i >= 0 :
        commits[i].append(a)
    else:
        commits.append([(a[3],a[5],a[2])])
        commits[i].append(a)
    return commits


if __name__ == '__main__':
    
    logfile = False

    opts, args = getopt.getopt(sys.argv[1:], 'fh', ["help", "output="])
    for o, a in opts:
        if o == "-f":
            logfile = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        else:
            assert False, "unhandled option"

    cmd = 'cvs log ' + ' '.join(args)
    print(cmd)

    with tempfile.TemporaryFile() as tmpout:
        p = subprocess.Popen(cmd, stdout=tmpout, shell=True)
        p.wait()
        if p.returncode != 0:
            print('cmd exit on ' + str(p.returncode))
            # continue ignore failed
            #sys.exit(1)
        tmpout.seek(0)
        log = tmpout.read()
        #print(log)

    pfile = re.compile(r'^RCS file:\s(.+?)[,|\n]', re.M)
    prev = re.compile(r'(^revision\s[0-9\.]+)', re.M)
    pdate = re.compile(r'^date:\s(.+?);', re.M)
    puser = re.compile(r'author:\s(.+?);')
    pchange = re.compile(r'lines:\s(.+?)\n')
    pdesc = re.compile(r'\n(^.*)\n[-|=]', re.M)

    idxl = []
    fl = []
    iterator = pfile.finditer(log)
    for m in iterator:
        #print m.span()
        idxl.append(m.span())
        #print m.groups()[0]
        fl.append(m.groups()[0])
    #print(idxl)

    l = []
    for i in range(len(idxl)):
        if i < len(idxl) - 1:
            s = log[idxl[i][1]:idxl[i+1][0]]
        else:
            s = log[idxl[i][1]:]
        #print(s)

        while True:
            m = prev.search(s)
            if not m:
                break
            rev = m.groups()[0]
            s = s[m.span()[1]:]
            #print(s)
            m = pdate.search(s)
            date = m.groups()[0]
            s = s[m.span()[1]:]
            #print(s)
            m = puser.search(s)
            user = m.groups()[0]
            s = s[m.span()[1]:]
            #print(s)
            m = pchange.search(s)
            change = ''
            if m:
                change = m.groups()[0]
                s = s[m.span()[1]-1:]
                #print(s)
            m = pdesc.search(s)
            desc = m.groups()[0]
            s = s[m.span()[1]:]
            #print(s)
            t = time.mktime(time.strptime(date, '%Y/%m/%d %H:%M:%S'))
            l.append((fl[i],rev,t,user,change,desc))
    #print(l)

    commits = []
    for a in l:
        commits = add2commit(commits, a)
    commits.sort(key = lambda x:str(x[0][2])+x[0][0], reverse=True)
    #print(commits)
    #for a in commits:
    #    print(a[0])
    #    for b in a[1:]:
    #        print(b)

    if not logfile:
        for a in commits:
            print('* ' + time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(a[0][2])) + ' - ' + a[0][0] + ' - ' + a[0][1])
    else:
        for a in commits:
            print('* ' + time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(a[0][2])) + ' - ' + a[0][0] + ' - ' + a[0][1])
            for b in a[1:]:
                #l.append((fl[i],rev,date,user,change,desc))
                print('|  ' + b[0] + '\t|' + b[4]  + (', ' if b[4] else '') + b[1] + ', ' + time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(b[2])))
