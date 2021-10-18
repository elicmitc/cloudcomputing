#!/bin/sh
# start the instance 
gcloud compute instances start server-instance --zone=us-west1-a
<<com
gcloud compute ssh server-instance --zone=us-west1-a --command='
	sudo apt-get -y install git && \
	curl -o server.py https://raw.github.iu.edu/elicmitc/cloudcomputing/master/cerver.py?token=AAACVZ6VZUKWWWXREESAFXDBOMYJ6 && \
	sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev \
		libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev \
		wget libbz2-dev && \
	wget https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tgz && \
	tar -xf Python-3.8.0.tgz && \
	cd Python-3.8.0 && \
	./configure --enable-optimizations && \ 
	make -j 8 && \
	sudo make altinstall && \
	cd ~/ && ls'
com

gcloud compute ssh server-instance --zone=us-west1-a --command='
	sudo apt-get -y install git && \
	curl -o server.py https://raw.github.iu.edu/elicmitc/cloudcomputing/master/cerver.py?token=AAACVZ6VZUKWWWXREESAFXDBOMYJ6 && \
	curl -o start.sh https://raw.github.iu.edu/elicmitc/cloudcomputing/master/startserver.sh?token=AAACVZ6XVNMWRYULHFS53WLBOX57E && \
	curl -o kill-zombie-server.py https://raw.github.iu.edu/elicmitc/cloudcomputing/master/kill-zombie-server.py?token=AAACVZZSWJY3E4ADHWGAAI3BOY7OA'
gcloud compute ssh server-instance --zone=us-west1-a 
