#!/usr/bin/python3
#coding=utf8

import sys
import re

def parse2dict(id,s,d):

    pat=re.compile(r'<.*?="(.*?)".*?>(.*?)<')
    m=pat.search(s)
    if not m:
        print(s)
    else:
        #print(id+'-'+m.group(1),m.group(2))
        d[id+'-'+m.group(1)]=m.group(2)

def gen2h(k,v):

    k=k.replace('.','_')
    return r'const char * '+k+'="'+v+'";\n'

if __name__ == '__main__':

    path1 = sys.argv[1]

    d={}
    lines = open(path1,'r').readlines()
    pat = re.compile(r'translatable="yes"')
    wl=[]
    pre = re.compile(r'<widget .*?id="(.*?)"')
    end = re.compile(r'</widget>')
    for file_line in lines:
        m=pre.search(file_line)
        if m:
            wl.append(m.group(1))
        m=end.search(file_line)
        if m:
            wl.pop()
        if pat.search(file_line):
            parse2dict(wl[-1],file_line,d)

    print(len(d))
    path2 = path1 + '.h'
    f2 = open(path2,'w')
    for k,v in d.items():
        print(k,v)
        s=gen2h(k,v)
        f2.write(s)
    f2.close()



