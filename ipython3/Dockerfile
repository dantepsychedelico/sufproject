FROM python:3.4.3

MAINTAINER Zac Chung

WORKDIR /home/python

ADD ipython-3.0.0.tar.gz /home/python

RUN cd ipython-3.0.0 && python3 setup.py install

ADD pip-6.0.8.tar.gz /home/python

RUN cd pip-6.0.8 && python3 setup.py install

VOLUME /home/python
