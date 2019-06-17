#!/usr/bin/env bash

set -e

ACCESS_KEY=$1
SECRET_ACCESS_KEY=$2

docker build -t hw07-vm-broker ./broker
docker build -t hw07-vm-storage ./storage

# create network if it doesn't exist
if [[ -z $(docker network ls --filter name=hw07 -q) ]]; then
    echo 'creating docker network....'
    docker network create --driver bridge hw07
fi

# must start mqtt broker first
docker run --rm --name broker --network hw07 -p 1883:1883 -d hw07-vm-broker
docker run --rm --name storage --network hw07 -d \
    -e COS_ENDPOINT=https://s3.us.cloud-object-storage.appdomain.cloud \
    -e MQTT_BROKER=broker \
    -e BUCKET=shane-w251 \
    -e AWS_ACCESS_KEY_ID=$ACCESS_KEY \
    -e AWS_SECRET_ACCESS_KEY=$SECRET_ACCESS_KEY \
    hw07-vm-storage
