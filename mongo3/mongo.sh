#!/bin/bash

cd $(dirname $0)
chcon -Rt svirt_sandbox_file_t $PWD

if [ "$2" != "" ]; then
	PORT=$(grep port: $2 | tr -d [:alpha:][:space:]:)
	NAME=$(echo $2 | sed 's/.conf$//')
	DBPATH=$(grep dbPath $2 | sed 's/[ ]*dbPath[: ]*//' | tr -d '"')
	if [ "$1" != "build" ] && [ "$PORT" == "" ]; then
		echo "config file no specify port"
		exit 1
	fi
	mkdir -p $DBPATH log
fi

case "$1" in
	build) 
		docker build -t mongo:3 .
		;;
	mongod | mongos) 
		docker run -d --net host --name $NAME \
			-v $PWD:/home/mongo mongo:3 $1 --config $2
		;;
	bash)
		docker run -it --net host --privileged --name bash -v $PWD:/home/mongo mongo:3 bash
		;;
	cleandb)
		rm -rf data/db/* data/configdb/*
		;;
	cleanlog)
		rm -f log/*
		;;
	*)
		echo "`basename $0` :usage: [build|mongod|mongos|cleandb|cleanlog] [config-file]"
		exit 1
		;;
esac

cd -
