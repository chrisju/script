#!/usr/bin/env bash

if [ -z $1 ]
then
    echo "usage: $0 imgpath"
    exit
fi

curl -F 'name=@./'$1 http://img.vim-cn.com/
