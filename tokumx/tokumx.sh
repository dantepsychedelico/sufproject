#!/bin/bash

if [ "$2" != "" ]; then
	PORT=$(grep port $2 | tr -d [:alpha:][:space:]=)
	NAME=$(echo $2 | sed 's/.conf//')
	if [ "$1" != "build" ] && [ "$PORT" == "" ]; then
		echo "config file no specify port"
		exit 1
	fi
fi

mkdir -p data/db data/configdb data/arb log

case "$1" in
	build) 
		docker build -t tokumx .
		;;
	mongod | mongos) 
		docker run -d --net="host" --name $NAME \
			-v $PWD:/home/tokumx tokumx \
			$1 --config $2
		;;
	cleandb)
		rm -f data/db/* data/configdb/*
		;;
	cleanlog)
		rm -f log/*
		;;
	*)
		echo "`basename $0` :usage: [build|mongod|mongos|cleandb|cleanlog] [config-file]"
		exit 1
		;;
esac
