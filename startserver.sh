#!/bin/sh
python3 kill-zombie-server.py>nul 2>&1 #suppress STDOUT and STDERR
rm nul
python3.8 server.py & PIDSER=$!
wait $PIDSER	#process id of server
echo "server connection terminated."
