#!/bin/bash

gphoto2 --set-config capturetarget=1

#curl "http://192.168.1.28:5000/m2?cw=1&step=200"

for i in {1..22}; do
    for k in {1..20}; do
        curl "http://192.168.1.28:5000/m1?cw=0&step=10"
        sleep 1
        gphoto2 --filename '/mnt/myvault/tmp/images/%Y%m%d%H%M%S%f.%C' --capture-image-and-download
        
    done
    curl "http://192.168.1.28:5000/m2?cw=1&step=15"
    sleep 2
done