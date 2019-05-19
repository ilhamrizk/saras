#!/bin/bash
sudo modprobe batman-adv
sudo ip link set wlo1 down
sudo ifconfig wlo1 mtu 1500
sudo iwconfig wlo1 mode ad-hoc
sudo iwconfig wlo1 essid my-mesh-network
sudo iwconfig wlo1 ap any
sudo iwconfig wlo1 channel 8
sleep 1s
sudo ip link set wlo1 up
sleep 1s
sudo batctl if add wlo1
sleep 1s
sudo ifconfig bat0 up
sleep 5s
# Use different IPv4 addresses for each device
# This is the only change necessary to the script for
# different devices. Make sure to indicate the number
# of bits used for the mask.
sudo ifconfig bat0 172.27.0.10/16
