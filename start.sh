#!/bin/bash
set -e

pkill python3 tor firefox.real
python3 /opt/pystock/main.py