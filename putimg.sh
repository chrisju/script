#!/usr/bin/env bash

if [ -z $1 ]
then
    echo "usage: $0 imgpath"
    exit
fi

#http_proxy=127.0.0.1:8087 curl -F 'name=@./'$1 https://img.vim-cn.com/
curl -F 'name=@./'$1 https://img.vim-cn.com/
