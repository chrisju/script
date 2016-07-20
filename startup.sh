#!/bin/bash

#stop shadowsocks with kill instead of ^c

#nohup pyupload >/dev/null 2>&1 &
nohup thunderbird >/dev/null 2>&1 &
nohup pidgin >/dev/null 2>&1 &
nohup /opt/longene/tm2013/tm2013.sh >/dev/null 2>&1 &
cd /mnt/DATA/upload;nohup python /home/zz/script/SimpleHTTPServerWithUpload.py >/dev/null 2>&1 &
nohup sslocal -c /etc/shadowsocks/config-puff.json >/dev/null 2>&1 &
exit 0

