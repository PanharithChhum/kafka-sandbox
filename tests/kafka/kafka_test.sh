#!/bin/bash

#create a kafka topic 'foobar'
sleep 30
kafka-topics.sh --create --zookeeper $KAFKA_ZOOKEEPER_CONNECT --replication-factor 1 --partitions 1 --topic foobar
