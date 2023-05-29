#!/bin/sh
# git clone https://www.github.com/kacperturon/microscope.git
# cd microscope/rpi
python -m pip install --upgrade pip
apt-get update
apt-get -y install libatlas-base-dev
python -m pip install -vI --prefer-binary -r requirements.txt
mkdir -p ./pictures
mkdir -p /.aws
echo "[default]
aws_access_key_id = AKIATFY4RCWECS3SFNNE
aws_secret_access_key = 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" > /.aws/credentials
# python -m flask --app snap2 run --host=0.0.0.0