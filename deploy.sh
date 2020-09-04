#!/bin/bash
Hostport=8080
Localport=8080
Network=bridge
docker rm $(docker stop $(docker ps -a -q --filter ancestor=pvpc_service --format="{{.ID}}"))
docker container rm pvpc_service

rm -Rf loggingbot
git clone https://github.com/Guillelerial/loggingbot.git

docker build --no-cache -t pvpc_service .
docker run --network=$Network --name pvpc_service -p $Hostport:$Localport pvpc_service
