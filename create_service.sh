#!/bin/bash

# check sudo permissions
if [ "$EUID" -ne 0 ]; then
  echo "please execute with root privileges:"
  echo "sudo ./create_service.sh"
  exit
fi

# get absolute path of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SERVICE_NAME="keycounter.service"

# add service to systemd
cat << EOF > /etc/systemd/system/$SERVICE_NAME
[Unit]
Description=KeyCounter Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 -u $SCRIPT_DIR/logkey.py
WorkingDirectory=$SCRIPT_DIR
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

# make systemctl aware of the new service
systemctl daemon-reload

# enable service to start on boot
systemctl enable $SERVICE_NAME

systemctl start $SERVICE_NAME

echo "Service $SERVICE_NAME created and started."
echo "To check its status, use: sudo systemctl status $SERVICE_NAME"