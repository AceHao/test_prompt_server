## Build the container

docker build -t prompt_ant .

## Run locally

docker run -p 9080:8080 -e SM_ASSIGNED_PRIVATE_IP_REV_2023_10=<ip-asigned-by-docker-bridge> -e ROUTING_TABLE_NAME=ABCTable -e ROUTING_ENTRY_KEY=xyzEp  -e AWS_ACCESS_KEY_ID=<your-key> -e AWS_SECRET_ACCESS_KEY=<your-secret> prompt_ant

if your docker bridge is not running anything, default value for ip-asigned-by-docker-bridge should be 172.17.0.2

## make_me_available()

curl localhost:9080/ping

on a production setting, this API will be called perdically by the service team for health checking purposes.

