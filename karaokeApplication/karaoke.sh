#!/bin/bash


# ubuntu
echo "Updating Packages"
sudo apt-get update  # To get the latest package lists
sudo apt-get install software-properties-common -y
sudo apt-add-repository universe


echo "Installing Python3"
sudo apt install python3 -y


echo "Installing NTFS Compatibility"
sudo apt-get install ntfs-3g -y


echo "installing pip"
sudo apt-get install python3-pip -y  #pip3
# sudo apt install python-pip -y #pip normal


echo "Installing Pandas"
pip3 install pandas
# pip install pandas


echo "Installing VLC"
sudo apt-get install vlc -y
pip3 install python-vlc
# pip install python-vlc


echo "Installing Tkinter"
sudo apt-get install python3-tk -y
# pip install pyttk


echo "Installing Flask"
pip3 install flask


echo "Installing Youtube DL"
pip3 install youtube_dl


#forçar saída de fone
amixer cset numid=3 1


#service para auto-bootar karaoke
sudo echo "[Unit]
Description=Sing Like Hell!
After=multi-user.target

[Service]
User=pi
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/pi/.Xauthority
ExecStart=/usr/bin/python3 /home/pi/karaokeApplication/vtokke.py
Restart=always
RestartSec=20s
KillMode=process
TimeoutSec=infinity

[Install]
WantedBy=multi-user.target" > /lib/systemd/system/karaoke.service




#service para auto-bootar API
sudo echo "[Unit]
Description=Karaoke API and Youtube DL
After=multi-user.target

[Service]
User=pi
ExecStart=/usr/bin/python3 /home/pi/karaokeApplication/catapy.py
Restart=always
RestartSec=10s
KillMode=process
TimeoutSec=infinity


[Install]
WantedBy=multi-user.target" > /lib/systemd/system/catapy.service


sudo systemctl daemon-reload

sudo systemctl enable karaoke.service

sudo systemctl enable catapy.service

#mydir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" > /dev/null && pwd )"

#sudo cp ../




echo "DIZ QUE EH VERDADE, QUE TEM SAUDAAAADEEE!"







# INSTALLER PRA MAC

#/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

#sudo easy_install pip

#sudo pip install --upgrade pip

#brew install python3

#brew install vlc



### TUDO CERTO ATÉ AQUI, DAQUI PRA FRENTE TESTANDO#####



#brew install lua

#sudo pip install python-vlc

#check se tem VLC na pasta


#wget https://get.videolan.org/vlc/3.0.8/macosx/vlc-3.0.8.dmg


#sudo hdiutil attach vlc-3.0.8.dmg


#sudo cp -R "/Volumes/VLC media player" .



#wget ftp://ftp.videolan.org/pub/videolan/vlc/3.0.7/vlc-3.0.7.tar.xz

#tar xvJf vlc-3.0.7.tar.xz

#cd vlc-3.0.7

#./configure





#etc.