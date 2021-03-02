#!/bin/bash

##Script to prepare Manjaro for PinePhone to use with the PineEye
##Installation log file "install_logs.txt" gets created in install_deps/logs/

logfile=logs/log_file.txt		#File to be used to log installation process

formatdate=$(date +"%m_%d_%Y_%R")
date -u > $logfile

#Prepare directories
mkdir -p logs

#Update and upgrade system packages
function update_upgrade() { 	
  sudo pacman -Syy >> $logfile  	#Update repositories cache
  sudo pacman -Syu -y >> $logfile  	#Upgrade packages
}

#Installation of Docker if using Baremetal
function install_enable_docker() {
  ##Docker
  sudo pacman -S docker -y >> $logfile			#Install Docker
  sudo systemctl start docker.service >> $logfile	#Start Docker service
  sudo systemctl enable docker.service >> $logfile	#Enable Docker service
  docker_version=$(sudo docker version)
  echo "Docker version isntalled: $docker_version " >> $logfile
}

#Installation of I2C tools. 
function install_i2c_tools() {
  sudo pacman -S i2c-tools -y >> $logfile
}

#Installation of Python tools
function isntall_python_tools() {
  sudo pacman -S python-smbus -y >> $logfile
}


#Appending date to logfile name
mv $logfile ${logfile}_${date}
