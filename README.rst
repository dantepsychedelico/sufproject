sufproject
==========

build tokumx with docker

.. code-block:: bash

    $ cd tokumx
    $ ./tokumx.sh build

create mongod container

.. code-block:: bash

    $ ./tokumx.sh mongod tokumx.conf


::

    ## new id
    CLIENT {"method": "new"}
    SERVER {"status": "ok", "method": "new", "id": 1}
    ## online
    CLIENT {"method": "online", "id": 1}
    SERVER {"status": "ok", "method": "online"}
    ## new room
    CLIENT {"method": "newroom", "id": 1, "roomname": "myFirstRoom", "alivetime": 1000}
    SERVER {"status": "ok", "method": "newroom", "roomid": 1, "roomname": "myFirstRoom", "members": [1], "createtime": 1234, "alivetime": 1000}
    ## join room
    CLIENT {"method": "join", "id":2, "roomid": 1}
    SERVER {"status": "ok", "method": "join", "roomid": 1, "roomname": "myFristRoom", "createtime": 1234, "alivetime": 1000}
    ## user that id is 1 chat in room with roomid is 1
    CLIENT with id is 1 {"method": "chat", "roomid": 1, "id": 1, "type": "content", "content": "hello, I'm Zac"}
    SERVER to CLIENT(id=1) {"status": "ok", "method": "chat", "id": 1}
    SERVER to CLIENT(id=2) {"status": "ok", "method": "chat", "roomid": 1, "id": 1, "type": "content", "content": "hello, I'm Zac", time: 1234}

