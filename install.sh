#!/bin/bash

apt install -y python3.10-venv

python3 -m venv .venv

source .venv/bin/activate

pip3 install -r requirements.txt

chmod +x run.sh

cp system-resources-api.service /etc/systemd/system/system-resources-api.service

systemctl daemon-reload

systemctl restart system-resources-api

