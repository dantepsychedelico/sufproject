FROM debian:wheezy

# add our user and group first to make sure their IDs get assigned consistently, regardless of whatever dependencies get added
#RUN groupadd -r mongodb && useradd -r -g mongodb mongodb

RUN apt-get update \
	&& apt-get install -y curl numactl \
	&& rm -rf /var/lib/apt/lists/*

# grab gosu for easy step-down from root
RUN gpg --keyserver pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4
RUN curl -o /usr/local/bin/gosu -SL "https://github.com/tianon/gosu/releases/download/1.2/gosu-$(dpkg --print-architecture)" \
	&& curl -o /usr/local/bin/gosu.asc -SL "https://github.com/tianon/gosu/releases/download/1.2/gosu-$(dpkg --print-architecture).asc" \
	&& gpg --verify /usr/local/bin/gosu.asc \
	&& rm /usr/local/bin/gosu.asc \
	&& chmod +x /usr/local/bin/gosu

ENV TOKUMX_RELEASE_FINGERPRINT 505A7412
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key $TOKUMX_RELEASE_FINGERPRINT

ENV TOKUMX_VERSION 2.4.10

RUN echo "deb [arch=amd64] http://s3.amazonaws.com/tokumx-debs wheezy main" \
	| tee /etc/apt/sources.list.d/tokumx.list \
	&& apt-get update \
	&& apt-get install -y tokumx

WORKDIR /home/tokumx

VOLUME /home/tokumx

