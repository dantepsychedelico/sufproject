# python-socket-server
# 
# version: 0.2
# 
FROM python:3.4.3

MAINTAINER Zac Chung

#RUN groupadd -r python && useradd -r -g python python

#RUN mkdir -p /home/python/log && chown -R python:python /home/python
RUN mkdir -p /home/python/log

RUN pip3 install pymongo

ENV VERSION 0.3
ENV PORT 30000
ENV HOST 0.0.0.0
ENV LOG_FILE log/python-server.log

COPY *.py /home/python/

WORKDIR /home/python

#USER python

VOLUME /home/python/log

CMD ["python3", "server.py"]
