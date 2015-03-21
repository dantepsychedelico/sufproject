FROM python:3.4.3

MAINTAINER Zac Chung

WORKDIR /home/python

ADD pymongo-2.8.tar.gz /home/python
RUN cd pymongo-2.8 && python3 setup.py install

VOLUME /home/python

