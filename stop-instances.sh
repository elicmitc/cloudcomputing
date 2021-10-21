#!/bin/sh
gcloud compute instances stop client-instance --zone=us-west1-a
gcloud compute instances stop server-instance --zone=us-west1-a
