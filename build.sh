#!bin/bash
# build.sh

# install mesh network
#sudo apt-get update
#sudo apt-get install libnl-3-dev libnl-genl-3-dev -y
cd /etc
sudo git clone https://github.com/ilhamrizk/saras.git
cd batctl
sudo make install
sudo cp /etc/saras/mesh/mesh.sh /mesh.sh
sudo chmod 700 /mesh.sh
sudo cp /etc/saras/mesh/sysctl.conf sysctl.conf
sudo apt-get -y install hostapd dnsmasq

#
sudo cp /etc/saras/mesh/mesh.service /etc/systemd/system/mesh.service
sudo systemctl daemonreload
sudo systemctl enable mesh.service
sudo systemctl disable dhclient
sudo systemctl disable NetworkManager
sudo systemctl disable networking
sudo systemctl disable wpa_supplicant
sudo reboot
