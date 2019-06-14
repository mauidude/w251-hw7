#!/usr/bin/env bash

docker stop detector
docker stop forwarder
docker stop broker

docker network rm hw03
