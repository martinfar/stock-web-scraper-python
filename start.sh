#!/bin/bash
set -e

pkill python3
pkill tor
pkill firefox.real

python3 /opt/pystock/main.py