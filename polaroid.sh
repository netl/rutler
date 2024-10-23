#!/usr/bin/env bash

picturedir=~/Pictures

while :
do
    inotifywait -e close_write $picturedir/
    timestamp=$(date +%s)
    mv $picturedir/$(ls $picturedir/ -t | head -n 1) ~/archive/$timestamp.jpg
    #bluetooth-sendto --device=C8:58:95:60:26:37 ~/archive/$timestamp.jpg
done
