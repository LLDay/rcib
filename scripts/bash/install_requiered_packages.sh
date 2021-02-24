#!/usr/bin/env bash

if pacman --version; then
    pacman -S python3 python3-pip --noconfirm

elif apt-get --version; then
    apt-get update
    apt-get -y install python3 python3-pip
    if ! dpkg --compare-versions "$(python3 --version 2>&1 | awk '{ print $2 }' )" 'gt' '3.6.0'; then
        apt-get -y install software-properties-common python-software-properties
        add-apt-repository -y ppa:deadsnakes/ppa
        apt-get update
        apt-get -y install python3.7 python3.7-venv
        python3.7 -m ensurepip --upgrade
    fi

else
    echo "Unkown package manager"
    exit 1
fi
