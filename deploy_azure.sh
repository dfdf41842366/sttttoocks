#!/bin/bash
RG="stock-hunter-rg"
ACI="stock-hunter-api"
IMG="stockhunter:latest"
docker build -t $IMG .
az group create --name $RG --location eastus
az container create --resource-group $RG --name $ACI \
  --image $IMG \
  --cpu 2 --memory 4 \
  --ports 8000 \
  --ip-address public
echo "Check logs: az container logs -g $RG -n $ACI"
