#!/bin/bash

#check necessary environment variables
[ -z "$KAFKA_ADVERTISED_HOST_NAME" ] && { echo "Need to set STATE"; exit 1; }

#create a kafka topic 'foobar'
kafka-topics.sh --create --zookeeper $KAFKA_ZOOKEEPER_CONNECT --replication-factor 1 --partitions 1 --topic foobar
