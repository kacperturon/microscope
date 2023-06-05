#!/bin/sh
# git clone https://www.github.com/kacperturon/microscope.git
# cd microscope/rpi
python -m pip install --upgrade pip
apt-get update
apt-get -y install libatlas-base-dev
python -m pip install -vI --prefer-binary -r requirements.txt
mkdir -p ./pictures
mkdir -p ~/.aws

# python -m flask --app snap run --host=0.0.0.0
# crontab -e
# ngrok http 500
# ngrok tcp 22