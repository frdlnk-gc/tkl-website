#!/bin/bash
# Ganzseiten-Screenshot: tools/shoot.sh <pfad> <breite> <hoehe> <ausgabe.png>
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --virtual-time-budget=6000 "--screenshot=$4" --window-size=$2,$3 "http://localhost:8771$1" >/dev/null 2>&1
