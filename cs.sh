#!/bin/sh
# cs.sh
find . -name "*.h" -o -name "*.c" -o -name "*.cpp" -o -name "*.cc" > cscope.files
cscope -bq
ctags -R --languages=c
