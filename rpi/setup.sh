#!/bin/sh

# git clone https://www.github.com/kacperturon/microscope.git
# cd microscope/rpi
python -m pip install --upgrade pip
apt-get update
sudo apt-get -y install libatlas-base-dev
python -m pip install --no-cache-dir --prefer-binary -r requirements.txt
mkdir -p ./pictures
mkdir -p ~/.aws
mkdir -p ~/config/ngrok
# setup ngrok
cd ~/Downloads
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm.zip 
unzip ngrok-v3-stable-linux-arm.zip
sudo cp ngrok /usr/bin/ngrok
cd ~/microscope/rpi
# cat ngrok.conf >> ~/.config/ngrok/ngrok.yml
# ngrok authtoken {bitwarden-ngrok-token}
# echo "aws credentials" >> ~/.aws/credentials
# killall ngrok
# sudo echo "sh ~/microscope/rpi/startup.sh" > /etc/rc.local
# @reboot sh ~/microscope/rpi/startup.sh