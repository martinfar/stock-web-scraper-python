#!/bin/bash
set -e
echo "Deleting Old Files"
find /opt/pystock/stock-results/ -type f -mtime +1 -name '*.png' -execdir rm -- '{}' \;

pkill python3
pkill tor
pkill firefox.real

python3 /opt/pystock/main.py