#!/bin/sh
python3.8 server.py & PIDSER=$!
wait $PIDSER	
echo "server connection terminated."
