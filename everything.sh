#!/bin/sh
while getopts "c:" opt
do
	case "$opt" in
		c ) 	paramC="$OPTARG"
		    	gcloud compute instances create $paramC-instance --zone=us-west1-a --network my-default 
		    	wait 
			bash clie.sh -c $paramC-instance & PIDNEW=$!
			wait $PIDNEW
			echo 'closing $paramC client..'
			exit 0 ;;

	esac
done

gcloud compute instances create client-instance server-instance --zone=us-west1-a --network my-default & PIDCREATE=$!
wait $PIDCREATE
gcloud compute firewall-rules create myport12345 --allow tcp:12345 --direction=EGRESS 
gcloud compute firewall-rules create tcp12345 --allow tcp:12345 

bash serv.sh & PIDSERV=$! 
bash clie.sh & PIDCLIE=$!
wait $PIDCLIE
wait $PIDSERV
#gcloud compute instances stop client-instance --zone=us-west1-a
#gcloud compute instances stop server-instance --zone=us-west1-a
#gcloud compute instances list & PIDLIST=$!
wait $PIDLIST
echo "server/client operation terminated."
