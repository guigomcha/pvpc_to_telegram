#!/bin/bash

docker rm $(docker stop $(docker ps -a -q --filter ancestor=pvpc_service --format="{{.ID}}"))
docker container rm pvpc_service

rm -Rf loggingbot
git clone https://github.com/Guillelerial/loggingbot.git

docker build --no-cache -t pvpc_service .

