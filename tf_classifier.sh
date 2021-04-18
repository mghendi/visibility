#!/usr/bin/env bash

. /home/pi/myenv/bin/activate
cd /home/pi/Desktop/mlproject
python /home/pi/Desktop/mlproject/label_image.py /home/pi/Desktop/mlproject/image1.jpg
deactivate