#!/bin/sh

python -m pip install --upgrade pip
apt-get update
apt-get -y install libatlas-base-dev
python -m pip install -vI --prefer-binary -r requirements.txt
mkdir -p ./pictures
mkdir -p ~/.aws

# @reboot sh ~/microscope/rpi/startup.sh
# git clone https://www.github.com/kacperturon/microscope.git
# ngrok auth
# echo "aws credentials" > ~/.aws/credentials
# cd microscope/rpi
# nohup python -m flask --app snap run --host=0.0.0.0 2>&1 &
# crontab -e
# ngrok http 500
# ngrok tcp 22