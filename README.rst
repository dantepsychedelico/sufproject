sufproject
==========

build tokumx with docker

.. code-block:: bash

    $ cd tokumx
    $ ./tokumx.sh build

create mongod container

.. code-block:: bash

    $ ./tokumx.sh mongod tokumx.conf


Docker for mongo server
-----------------------
.. code-block:: bash

   # build docker mongo server
   $ docker pull mongo:3
   $ chcon -Rt svirt_sandbox_file_t data
   $ docker run -d --name suf_mongo -v $PWD/data:/data/db mongo:3


Docker for python socket server 
-------------------------------

.. code-block:: bash

   # build docker python socket server
   $ cd socketServer
   $ docker build -t python-socket-server:0.3 .
   # run server
   $ docker run -d --name python-socket-server-0.3 --link suf_mongo:db -v $PWD/log:/home/python/log -p 30000:30000 python-socket-server:0.3

python socket server framework

::

    socketServer
    ├── Dockerfile
    ├── log
    │   └── python-server.log                   ## the socket server log file location
    ├── mongoCtrl.py                            ## mongodb controller
    ├── mongoModel.py                           ## mongodb model, connect to mongo
    ├── router.py                               ## the method's router
    ├── server.py                               ## main socket server
    ├── socketProtocal.py                       ## socket server protocal
    ├── test
    │   ├── socketTest.py
    │   ├── testConnect-1.py
    │   └── testingFormat.txt                   ## json's format
    └── Users.py                                ## store sockets' conneciton of the online user

