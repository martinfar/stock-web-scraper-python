#!/bin/bash
set -e

tor -f /etc/tor/torrc & 
cron -f -l 2 &

while ! (curl --stderr - --socks5-hostname 127.0.0.1:9050 https://check.torproject.org/ | grep -q 'This browser is configured to use Tor' ; ) do   
  sleep 1 # wait for 1/10 of the second before check again
  echo "wait for tor to open "
done

# if [[ -z "${SCHEDULE}" ]]; then
#   python3 /opt/pystock/main.py
# else
#   exec go-cron "$SCHEDULE" python3 /opt/pystock/main.py
# fi

python3 /opt/pystock/main.py

exec "$@"
