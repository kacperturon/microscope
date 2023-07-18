#!/bin/sh

# sudo apt-get update
# sudo apt-get install git -y
# git clone https://www.github.com/kacperturon/microscope.git
# cd microscope/rpi
# chmod +x setup.sh startup.sh
# chmod +x -R helpers/
python -m pip install --upgrade pip
sudo apt-get -y install libatlas-base-dev
python -m pip install --no-cache-dir --prefer-binary -r requirements.txt
mkdir -p ./pictures
mkdir -p ~/.aws
mkdir -p ~/.config/ngrok
# setup ngrok
cd ~/Downloads
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm.zip 
unzip ngrok-v3-stable-linux-arm.zip
sudo cp ngrok /usr/bin/ngrok
cd ~/microscope/rpi

# STEPS:
# replace /etc/wpa_supplicant/wpa_supplicant.conf with wpa_supplicant.conf
# sudo wpa_cli -i wlan0 reconfigure
# replace token in ngrok.conf and:
#   echo "ngrok.conf" >>  ~/.config/ngrok/ngrok.yml
# copy and execute aws_credentials.txt
# crontab -e
# @reboot cd /home/micro/microscope/rpi && sh /home/micro/microscope/rpi/startup.sh
# add environment variables to /etc/environment & reset ssh call

# EXTRAS:
# killall ngrok
# sudo reboot
# sudo dd if=./microscope16shrink.img of=/dev/sdc bs=32M status=progress
# sudo dd bs=4M if=/dev/sdc of=/home/username/MyImage.img status=progress