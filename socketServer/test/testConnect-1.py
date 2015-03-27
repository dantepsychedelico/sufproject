#!/usr/bin/env python3
#
# the e2e testing
from sys import argv
from socketTest import socketTest
import time
from unittest import TestCase
tc = TestCase()

HOST = argv[1] if len(argv) > 1 else "127.0.0.1"
PORT = int(argv[2]) if len(argv) > 2 else 30000

st = socketTest(HOST, PORT)
st.connect()
## test new
res = st.producer({"method": "new"}).comsumer()
uid = res.pop("uid")
sid = res.pop("sid")
tc.assertDictEqual(res, {"status": "ok", "method": "new"})

## test online
res = st.producer({"method": "online", "uid": uid}).comsumer()
tc.assertEqual(res.pop("uid"), uid)
tc.assertDictEqual(res, {"status": "ok", "method": "online"})

## test new room
alivetime = 1000
roomname = "myFirstRoom"
res = st.producer({"method": "newroom", "uid": uid, "roomname": roomname, "alivetime": alivetime}).comsumer()
roomid = res.pop("roomid")
createtime = res.pop("createtime")
tc.assertDictEqual(res, {"status": "ok", "method": "newroom"})

## 10s threshold
tc.assertLessEqual(createtime, int(time.time()))   
tc.assertGreater(createtime, int(time.time())-10)

## test join room
st.disconnect()
st.connect()
res = st.producer({"method": "new"}).comsumer()
uid2 = res.pop("uid")
sid2 = res.pop("sid")
tc.assertEqual(res, {"status": "ok", "method": "new"})
res = st.producer({"method": "join", "uid": uid, "roomid": roomid}).comsumer()
roomid2 = res.pop("roomid")
tc.assertEqual(roomid2, roomid)
createtime2 = res.pop("createtime")
tc.assertEqual(createtime2, createtime)
alivetime2 = res.pop("alivetime")
tc.assertEqual(alivetime2, alivetime)
members = res.pop("members")
members.sort()
tc.assertEqual(members, [uid, uid2])
tc.assertDictEqual(res, {"status": "ok", "method": "join", "roomname": roomname})
st.disconnect()
print("done")
