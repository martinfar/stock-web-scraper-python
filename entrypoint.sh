#!/bin/bash
set -e

tor -f /etc/tor/torrc & 

while ! nc -z localhost 9050; do   
  sleep 0.1 # wait for 1/10 of the second before check again
  echo "wait for tor to open "
done

tail -f /dev/null
#python3 /opt/pystock/main.py

exec "$@"
