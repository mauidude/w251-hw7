#!/usr/bin/env bash

docker stop storage
docker stop broker

docker network rm hw03
