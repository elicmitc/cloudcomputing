#!/bin/sh
while getopts "c:" opt
do
	case "$opt" in
		c ) 	paramC="$OPTARG" # paramC = {name}-instance 
			gcloud compute instances start $paramC --zone=us-west1-a
			gcloud compute ssh $paramC --zone=us-west1-a --command='\
			curl -o client.py https://raw.github.iu.edu/elicmitc/cloudcomputing/master/client.py?token=AAACVZYY7AL645B57VQQEMLBONAPY'
			gcloud compute ssh $paramC --zone=us-west1-a & PIDNEW=$!
			wait $PIDNEW
			echo 'closing $OPTARG client..'
			exit 0
			;;
	esac
done
gcloud compute instances start client-instance --zone=us-west1-a
gcloud compute ssh client-instance --zone=us-west1-a --command='\
	sudo apt-get install git && \
	curl -o client.py https://raw.github.iu.edu/elicmitc/cloudcomputing/master/client.py?token=AAACVZYY7AL645B57VQQEMLBONAPY && \'
gcloud compute ssh client-instance --zone=us-west1-a 
