#!/bin/sh

nohup ngrok start --all &
nohup python -m flask --app /home/micro/microscope/rpi/snap run --host=0.0.0.0 2>&1 &