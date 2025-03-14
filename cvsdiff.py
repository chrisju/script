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
from decimal import Decimal
from datetime import datetime
from distutils.version import LooseVersion

# simply show cvs diffs
# cvsshow
# cvsshow HEAD~~
# cvsdiff HEAD~ HEAD~~~
# cvsdiff HEAD~~~ HEAD
# cvsdiff


def usage():
    print(
'''\
usage: %s [--diff] [COMMIT] [COMMIT2] [PATH]...
'''
% (sys.argv[0])
    )

def getver(version, shift):
    prev, suff = version.split('.')
    a = Decimal(suff) + Decimal(shift)
    return prev + '.' + str(a)

def runcmd(cmd, hideStderr = False):
    print(cmd)
    if hideStderr:
        with tempfile.TemporaryFile() as tmpout, tempfile.TemporaryFile() as tmperr:
            p = subprocess.Popen(cmd, stdout=tmpout, stderr=tmperr, universal_newlines=True, shell=True)
            p.wait()
            tmpout.seek(0)
            tmperr.seek(0)
            if p.returncode != 0:
                print(tmperr.read())
                print('cmd exit on ' + str(p.returncode))
                sys.exit(1)
            return tmpout.read(), tmperr.read()
    else:
        with tempfile.TemporaryFile() as tmpout:
            p = subprocess.Popen(cmd, stdout=tmpout, universal_newlines=True, shell=True)
            p.wait()
            if p.returncode != 0:
                print('cmd exit on ' + str(p.returncode))
                sys.exit(1)
            tmpout.seek(0)
            return tmpout.read(), None

def getcvslog(path):
    cmd = 'python /home/outer2/g-zhuwei/bin/cvslog.py -f ' + path
    # slow cmd with stderr output, so do not hide stderr output
    log, _ = runcmd(cmd, hideStderr = False)
    #print(log)
    return log

def getcvscommits(path):
    # get cvslog for path
    log = getcvslog(path)
    # get commits for path
    commits = []
    lines = log.splitlines()
    for line in lines:
        if line.startswith('*'):
            commits.append([])
        elif line.startswith('|'):
            m = plogfile1.search(line)
            filepath = m.group(1)
            headversion = m.group(2)
            commits[-1].append((filepath, headversion))
    return commits

def getcommitindex(commits, lver, remotemode):
    if remotemode:
        # get index of remote.head
        headidx = 0
    else:
        # get cvs status
        # localver,localtime,remotever,file
        sts = getcvsstatus(path)

        # get index of local.head
        sts.sort(key=lambda x: x[1])
        newest = sts[-1]
        #print('newest:', newest)
        for i in range(len(commits)):
            commit = commits[i]
            #print(commit)
            for fst in commit:
                if newest[3] == fst[0] and newest[0] == fst[1]:
                    headidx = i

    # get commit
    shift = len(lver) - len('HEAD')
    return headidx + shift

def getcommit(commits, lver, remotemode):
    return commits[getcommitindex(commits, lver, remotemode)]

def getcvsstatus(path):
    cmd = 'cvs status ' + path
    log, _ = runcmd(cmd, hideStderr = True)
    l = []
    ms = pstatus.finditer(log)
    for m in ms:
        # localver,localtime,remotever,file
        sttime = datetime.strptime(m.group(2), "%a %b %d %H:%M:%S %Y")
        l.append((m.group(1), sttime, m.group(3), m.group(4)))
    return l

def getrealver(filepath, commit1, commit2, remotemode):
    shift1 = len('HEAD') - len(commit1)
    shift2 = len('HEAD') - len(commit2)

    # get cvs status
    # localver,localtime,remotever,file
    sts = getcvsstatus(filepath)
    head, _, rhead, _ = sts[0] 
    if remotemode:
        ver1 = getver(rhead, shift1)
        ver2 = getver(rhead, shift2)
    else:
        ver1 = getver(head, shift1)
        ver2 = getver(head, shift2)
    if not commit2:
        ver2 = None
    return ver1, ver2

def cvsdiff(path, ver1, ver2, extra):
    if ver2 and LooseVersion(ver2) < LooseVersion('1.2') :
        return
    if ver1 and LooseVersion(ver1) < LooseVersion('1.1') :
        ver1 = '1.1'

    s1 = '-r %s' % (ver1) if ver1 else ''
    s2 = '-r %s' % (ver2) if ver2 else ''
    cmd = 'cvs diff %s %s %s' % (s1, s2, path)
    if extra:
        cmd = '%s | %s' % (cmd, extra)
    cmd += ' | less -R'
    print(cmd)
    os.system(cmd)


if __name__ == '__main__':
    
    diffmode = False
    remotemode = False
    diff2updated = False
    extra = ''
    realvers = []

    print(' '.join(sys.argv))
    opts, args = getopt.getopt(sys.argv[1:], 'he:r:', ["diff", "remote", "updated", "help"])
    for o, a in opts:
        if o in ("--diff",):
            diffmode = True
        elif o in ("--remote",):
            remotemode = True
        elif o in ("--updated",):
            diff2updated = True
        elif o in ("-e",):
            extra = a
        elif o in ("-r",):
            realvers.append(a)
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        else:
            print("unhandled option")
            usage()
            sys.exit(1)

    pcommit = re.compile(r'^HEAD~*$')
    plogfile1 = re.compile(r'^\|\s+(.+?)\s+\|.*?revision\s([0-9\.]+),', re.M)
    pstatus = re.compile(r'Working revision:\s+([0-9\.]+)\s+(.+?)\n\s+Repository revision:\s+([0-9\.]+)\s+(.+?),v', re.M)

    paths = []
    commit1 = ''
    commit2 = ''
    if len(args) > 0:
        m = pcommit.search(args[0])
        if m:
            commit1 = args[0]
        else:
            paths = args
            args = []
    if len(args) > 1:
        m = pcommit.search(args[1])
        if m:
            commit2 = args[1]
            paths = args[2:]
        else:
            paths = args[1:]
    #print('commits:', commit1, commit2)
    if not paths:
        paths.append('.')

    # get relative cvs dir
    with open('CVS/Repository') as f:
        # must strip
        cvsdir = f.read().strip()

    for path in paths:
        isdir = False
        if os.path.isdir(path):
            isdir = True

        # show mode
        if not diffmode:
            # cvsshow -r x.x -r x.x file
            if realvers:
                ver1 = getver(realvers[0], -1)
                ver2 = realvers[0]
                cvsdiff(path, ver1, ver2, extra)

            else:
                # get all commits for path
                commits = getcvscommits(path)

                # get commit
                if not commit1:
                    commit1 = 'HEAD'
                commit = getcommit(commits, commit1, remotemode)

                # gen cvs diff cmd for show
                for filepath, version in commit:
                    relpath = filepath[filepath.find(cvsdir) + len(cvsdir + '/'):]
                    cvsdiff(relpath, getver(version, -1), version, extra)

        # diff mode
        else:
            if isdir:
                if realvers:
                    print('not support cvs diff -r x.x dir.')
                    sys.exit(1)

                cmd = 'cvs -qn update ' + path
                stdout, _ = runcmd(cmd, hideStderr = True)
                lines = stdout.splitlines()
                if commit1:
                    st = {relpath: status for line in lines for status, relpath in [line.split()]}
                    #for line in lines:
                    #    status, relpath = line.split()
                    #    if status == 'M':
                    #        print(line)
                    #        print('not support cvs diff dir with version when dir is dirty.')
                    #        sys.exit(1)

                    # diff between version and HEAD
                    # get all commits for path
                    commits = getcvscommits(path)

                    # get commit
                    idx1 = getcommitindex(commits, commit1, remotemode)
                    if commit2:
                        idx2 = getcommitindex(commits, commit2, remotemode)
                    else:
                        idx2 = getcommitindex(commits, 'HEAD', remotemode)

                    # get changed files between idx1 and idx2
                    # [idx1+1...idx2]
                    # {path:[ver],}
                    d = {}
                    for i in range(idx1 - 1, idx2 - 1, -1):
                        commit = commits[i]
                        for filepath, version in commit:
                            if filepath not in d:
                                d[filepath] = []
                            d[filepath].append(version)
                    for filepath, vers in d.items():
                        relpath = filepath[filepath.find(cvsdir) + len(cvsdir + '/'):]
                        ismodified = relpath in st and st[relpath] == 'M'
                        if not commit2 and ismodified:
                            cvsdiff(relpath, getver(vers[0], -1), None, extra)
                        else:
                            cvsdiff(relpath, getver(vers[0], -1), vers[-1], extra)

                # not commit1
                else:
                    for line in lines:
                        #print(line)
                        status, relpath = line.split()
                        if diff2updated:
                            # diff between local HEAD and remote HEAD
                            if status == 'U':
                                print(line)
                                # get cvs status
                                # localver,localtime,remotever,file
                                sts = getcvsstatus(relpath)
                                # no working ver if new file
                                if sts:
                                    head, _, rhead, _ = sts[0] 
                                    cvsdiff(relpath, head, rhead, extra)
                        else:
                            # diff to local HEAD
                            if status == 'M':
                                print(line)
                                cvsdiff(relpath, None, None, extra)

            # diff between ver1 and ver2 for file
            elif commit2 or len(realvers) == 2:
                # get ver1 and ver2
                if realvers:
                    ver1, ver2 = realvers
                else:
                    ver1, ver2 = getrealver(path, commit1, commit2, remotemode)
                cvsdiff(path, ver1, ver2, extra)

            # diff between localHEAD/ver1 and working version for file
            else:
                relpath = path
                if commit1 or realvers:
                    # diff between ver1 and working version for file
                    if commit1:
                        ver1, _ = getrealver(relpath, commit1, commit2, remotemode)
                    else:
                        ver1 = realvers[0]
                    cvsdiff(path, ver1, None, extra)
                else:
                    if diff2updated:
                        # diff between local HEAD and remote HEAD for file
                        # get cvs status
                        # localver,localtime,remotever,file
                        sts = getcvsstatus(relpath)
                        head, _, rhead, _ = sts[0] 
                        cvsdiff(relpath, head, rhead, extra)
                    else:
                        # diff between local HEAD and working version for file
                        cvsdiff(relpath, None, None, extra)
