#!/bin/sh

#install as per http://ipython.org/ipython-doc/dev/interactive/htmlnotebook.html
sudo apt-get install python-software-properties
sudo add-apt-repository ppa:chris-lea/zeromq
sudo add-apt-repository ppa:chris-lea/libpgm
sudo apt-get update
sudo apt-get install libzmq1
sudo apt-get install libzmq-dev
sudo apt-get install libpgm-5.1-0
sudo apt-get install python-pip
sudo apt-get install gcc
sudo apt-get install python-dev
sudo apt-get install g++
sudo apt-get install libpng-dev libjpeg8-dev libfreetype6-dev

sudo pip install pyzmq
 
sudo pip install tornado
sudo pip install --upgrade ipython
sudo pip install numpy
#sudo apt-get install python-scipy
sudo pip install scipy
sudo pip install matplotlib
ipython profile create nbserver
python -c "import IPython.lib; pw = IPython.lib.passwd(); print pw" 
echo "Edit the config, ie"
echo "jed /home/ubuntu/.ipython/profile_nbserver/ipython_notebook_config.py"

sudo pip install pyzmq

openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.pem -out ~/.ipython/mycert.pem

#install scikit-learn, from http://scikit-learn.org/stable/install.html
sudo apt-get install libatlas-dev 
sudo apt-get remove libatlas3gf-base libatlas-dev
sudo apt-get install libopenblas-dev
sudo pip install -U scikit-learn

#now run it, password is letmein
ipython notebook --profile=nbserver --cert=mycert.pem
