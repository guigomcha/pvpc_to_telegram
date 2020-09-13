#!/bin/bash
Hostport=8080
Localport=8080
Network=bridge

docker run  --name pvpc_service -p $Hostport:$Localport pvpc_service
docker network connect $Network pvpc_service
