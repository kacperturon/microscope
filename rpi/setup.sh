#!/bin/sh

# git clone https://www.github.com/kacperturon/microscope.git
# cd microscope/rpi
# chmod +x setup.sh startup.sh
python -m pip install --upgrade pip
apt-get update
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

# MANUAL:
# replace /etc/wpa_supplicant/wpa_supplicant.conf with 
# echo "wpa_supplicant" >> /etc/wpa_supplicant/wpa_supplicant.conf
# sudo wpa_cli -i wlan0 reconfigure
# replace token in ngrok.conf
# echo "ngrok.conf" >>  ~/.config/ngrok/ngrok.yml
# echo "aws credentials" >> ~/.aws/credentials
# sudo echo "sh /home/micro/microscope/rpi/startup.sh" > /etc/rc.local
# crontab -e
# @reboot cd /home/micro/microscope/rpi && sh /home/micro/microscope/rpi/startup.sh

# EXTRAS:
# killall ngrok
# sudo reboot