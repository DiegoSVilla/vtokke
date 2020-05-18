#!/bin/bash

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