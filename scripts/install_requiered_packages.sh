#!/usr/bin/env bash

known_pm=("pacman" "apt-get")
packet_list=("python3" "python-pip" "python3-pip")
install_packets=()

if ! which which; then
    pacman -Sy && pacman -S which --noconfirm
fi

for packet in ${packet_list[*]}; do
    if ! which "$packet" &>/dev/null; then
        install_packets+=("$packet")
    fi
done

if [ ${#install_packets[*]} -eq 0 ]; then
    exit 0
fi


for pm in ${known_pm[*]}; do
    local_pm=$(which "$pm" &>/dev/null && echo "$pm" || echo "$local_pm")
done

if [ -z "$local_pm" ]; then
    echo "Cannot find packet manager"
    exit 1
fi

echo "Packets to install: ${install_packets[*]} using $local_pm"

case "$local_pm" in
    pacman)
        pacman -Sy
        for p in "${install_packets[@]}"; do
            pacman -S "$p" --noconfirm
        done
        ;;

    apt-get)
        apt-get update
        for p in "${install_packets[@]}"; do
            apt-get -y install "$p"
        done
        ;;
esac
