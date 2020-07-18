#!/bin/bash
# Automated installer script for foneutil
# https://github.com/am401/foneutil

# Check if required applications are present on the system script is running on
printf "Welcome to the foneutil install script.\n"
for x in python3 pip3; do
if ! command -v $x &> /dev/null; then
  printf "The script could not detect $x on your device. You will need to install $x to run this setup script."
  exit
fi
done

if [ ! -d foneutil ]; then
  mkdir foneutil
else
  printf "The foneutil directory already exists. Please select a different directory to run this install script from.\n"
  exit
fi

cd foneutil

# Clone the foneutil repo
printf "Downloading application files...\n"
#git clone https://github.com/am401/foneutil.git
curl -sL https://raw.githubusercontent.com/am401/foneutil/master/foneutil.py > foneutil.py
curl -sL https://raw.githubusercontent.com/am401/foneutil/master/requirements.txt > requirements.txt

# Change to the repo's directory to setup venv
printf "Setting up virtual environment and requirements...\n"

# Setup the venv
python3 -m venv env

# Install the requirements using pip
source env/bin/activate
pip3 install -r requirements.txt

# Cleanup and remove requirements.txt
rm requirements.txt
