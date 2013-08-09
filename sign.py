#!/usr/bin/python2

import os
import sys

def show_usage():

    print 'usage:\nsign.py [-k] apk\n-k\tkeep origin apk\nexample: sign.py comiz.pk' % ()

if __name__ == '__main__':

    #print sys.argv
    argc = len(sys.argv)
    if argc != 2 and argc != 3:
        show_usage()
        exit()

    keypath = '/mnt/DATA/proj/eclipse/Android/zzlab.keystore'
    keyname = 'zzlab.keystore'
    zipalign = '/opt/android-sdk/tools/zipalign'

    keep = False
    if sys.argv[1] == '-k':
        keep = True
    originapk = sys.argv[argc-1]
    pair = os.path.splitext(originapk)
    signedapk = pair[0]+'_signed'+pair[1]
    if not os.path.exists(originapk):
        print 'Error: No such file.'
        exit()
    if os.path.exists(signedapk):
        os.remove(signedapk)

    cmd = 'jarsigner -verbose -keystore "%s" -signedjar "%s" "%s" %s' % (keypath, 'tmpapk', originapk, keyname)
    print cmd
    if os.system(cmd) != 0:
        print 'failed'
        exit()

    cmd = '%s -v 4 "%s" "%s"' % (zipalign, 'tmpapk', signedapk)
    print cmd
    if os.system(cmd) != 0:
        print 'failed'
        exit()

    os.remove('tmpapk')
    if not keep:
        os.remove(originapk)
    print 'ok'


