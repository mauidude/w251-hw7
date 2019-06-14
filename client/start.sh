#!/usr/bin/env bash
set -e

REMOTE_BROKER=$1

# build each docker image
docker build -t hw03-jetson-detector ./detector
docker build -t hw03-jetson-broker ./broker
docker build -t hw03-jetson-forwarder ./forwarder

# create network if it doesn't exist
if [[ -z $(docker network ls --filter name=hw03 -q) ]]; then
    echo 'creating docker network....'
    docker network create --driver bridge hw03
fi

# must start mqtt broker first
docker run --rm --name broker --network hw03 -p 1883:1883 -d hw03-jetson-broker

docker run --rm --name forwarder --network hw03 -e MQTT_OUTGOING_BROKER=$REMOTE_BROKER -d hw03-jetson-forwarder
docker run --rm --name detector --device=/dev/video1:/dev/video0 --network hw03 -d hw03-jetson-detector
