#!/bin/sh
echo "Server IP:"
read host
client="python3 client.py $host"
eval ${client} & PIDCL=$!
wait $PIDCL
echo "client closed.."
