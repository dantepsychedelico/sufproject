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
   $ docker run -d --name suf_mongo -v $PWD/data:/data/db mongo:3


Docker for python socket server 
-------------------------------

.. code-block:: bash

   # build docker python socket server
   $ cd socketServer
   $ docker build -t python-socket-server:0.3 .
   # run server
   $ docker run -d --name python-socket-server-0.3 --link suf_mongo:db -v $PWD/log:/home/python/log -p 30000:30000 python-socket-server:0.3



