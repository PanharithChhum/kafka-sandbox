#!/bin/bash

#populate correct env vars
# source ../env.sh

#test kafka
DOCKER_KAFKA_HOST=$(ipconfig getifaddr en0)
# printf "%-40s %-40s\n" "docker host ip:" "$DOCKER_KAFKA_HOST"

#pipe warning to /dev/null otherwise docker will complain that envvars defined in docker-compose are not set
KAFKA_ADVERTISED_HOST_NAME=$(docker-compose exec kafka bash -c 'echo "$KAFKA_ADVERTISED_HOST_NAME"' 2>/dev/null)

#check that $KAFKA_ADVERTISED_HOST_NAME is the correct ip address
#pipe to xargs to remove leading and trailing whitespace
if [[ "$KAFKA_ADVERTISED_HOST_NAME | xargs" != "$DOCKER_KAFKA_HOST | xargs" ]];
then 
	echo "kafka advertised host name is correct";
else
	echo "kafka advertised host name is incorrect"; exit 1;
fi 

#a hack because docker-compose does not support env like docker
docker-compose exec kafka env \
	DOCKER_HOST=$DOCKER_KAFKA_HOST \
	bash -c '/tests/kafka_test.sh' 
