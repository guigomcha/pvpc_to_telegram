#!/bin/bash
Hostport=8080
Localport=8080
Network=bridge

docker run  --network=$Network --name pvpc_service -p $Hostport:$Localport pvpc_service
