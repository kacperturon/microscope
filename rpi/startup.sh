#!/bin/sh

ngrok tcp 22
ngrok http 500
nohup python -m flask --app ~/microscope/rpi/snap run --host=0.0.0.0 2>&1 &