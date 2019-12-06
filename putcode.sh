#!/usr/bin/env bash

if [ -z $1 ]
then
    echo "usage: $0 codepath"
    exit
fi

#add ?<lang> or /<lang> to resulting url for line numbers and syntax highlighting
# if got  https://cfp.vim-cn.com/cbc
# open https://cfp.vim-cn.com/cbc/java for highlight version
curl -T $1 https://cfp.vim-cn.com/

