#!/bin/bash

if [ "$UID" = "0" ]
then
  apt-get update
  apt-get install -y ffmpeg libsm6 libxext6
else
  sudo apt-get update
  sudo apt-get install -y ffmpeg libsm6 libxext6
fi
