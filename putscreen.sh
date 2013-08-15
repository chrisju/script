#!/usr/bin/env bash

time=`date +%H:%M:%S` 
scrot -s "$time.png" -e "curl -sF 'name=@$time.png' http://eleveni386.7axu.com/Image/"

