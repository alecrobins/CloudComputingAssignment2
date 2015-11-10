#!/usr/bin/env bash

# installing mininet
result="$(
if cd mininet; then 
   printf "mininet already installed. moving on\n";
   cd ..
else 
  printf "updating repository sources and installing required packages\n";
  sudo apt-get -y update
  sudo apt-get -y upgrade
  sudo apt-get -y install git build-essential make
  printf "cloning mininet\n";
  sudo git clone git://github.com/mininet/mininet mininet; 
  printf "installing mininet\n";
  ./mininet/util/install.sh
fi
)"
printf "%s\n" " $result"

# making sure that mininet is available
sleep 10

# create the mininet topology and deploy our networking application on it
cd /vagrant
sudo python ./networking_application.py

