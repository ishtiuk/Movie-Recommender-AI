#!/usr/bin/env bash
# exit on error
set -o errexit

sudo apt-get update
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev
wget https://www.python.org/ftp/python/3.8.10/Python-3.8.10.tgz
tar -xf Python-3.8.10.tgz
cd Python-3.8.10
./configure --enable-optimizations
make && sudo make install


pip install --upgrade pip
pip install -r requirements.txt
