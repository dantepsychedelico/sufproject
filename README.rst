sufproject
==========

build tokumx with docker

.. code-block:: bash

    $ cd tokumx
    $ ./tokumx.sh build

create mongod container

.. code-block:: bash

    $ ./tokumx.sh mongod tokumx.conf

start server

.. code-block:: bash

   $ cd socketServer
   $ ./server.py
   ## or
   $ ./server.py <IP> <PORT>
