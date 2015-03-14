FROM debian:wheezy

MAINTAINER Zac Chung

RUN apt-get update \
	&& apt-get install -y curl numactl \
	&& rm -rf /var/lib/apt/lists/*

RUN curl -O http://downloads.mongodb.org/linux/mongodb-linux-x86_64-3.0.0.tgz && \
	tar -zxvf mongodb-linux-x86_64-3.0.0.tgz && \
	mv mongodb-linux-x86_64-3.0.0/bin/* /usr/bin

ENV MONGO_VERSION 3

WORKDIR /home/mongo

VOLUME /home/mongo

#RUN useradd -ms /bin/bash mongo

#USER mongo
