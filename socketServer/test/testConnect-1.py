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

st1 = socketTest(HOST, PORT)
st1.connect()
## test new
res = st1.producer({"method": "new"}).comsumer()
uid = res.pop("uid")
sid = res.pop("sid")
tc.assertDictEqual(res, {"status": "ok", "method": "new"})

## test online
st1.disconnect()
st1.connect()
res = st1.producer({"method": "online", "uid": uid}).comsumer()
tc.assertEqual(res.pop("uid"), uid)
tc.assertDictEqual(res, {"status": "ok", "method": "online"})

## test new room
alivetime = 1000
roomname = "myFirstRoom"
res = st1.producer({"method": "newroom", "uid": uid, "roomname": roomname, "alivetime": alivetime}).comsumer()
roomid = res.pop("roomid")
createtime = res.pop("createtime")
tc.assertDictEqual(res, {"status": "ok", "method": "newroom"})

## 10s threshold
tc.assertLessEqual(createtime, int(time.time()))   
tc.assertGreater(createtime, int(time.time())-10)

## test join room
st2 = socketTest(HOST, PORT)
st2.connect()
res = st2.producer({"method": "new"}).comsumer()
uid2 = res.pop("uid")
sid2 = res.pop("sid")
tc.assertEqual(res, {"status": "ok", "method": "new"})
res = st2.producer({"method": "join", "uid": uid, "roomid": roomid}).comsumer()
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

## test st2 send msg to st1
content = "hello, I'm Zac"
sendtime = int(time.time())
res2 = st2.producer({"method": "chat", "roomid": roomid2, \
        "uid": uid2, "mtype": "text", "content": content}).comsumer()
res = st1.comsumer()

time2 = res2.pop("time")
tc.assertLessEqual(time2, sendtime+5)
tc.assertGreaterEqual(time2, sendtime-5)
tc.assertDictEqual(res2, {"status": "ok", "method": "chat", "uid": uid2})

tc.assertEqual(res.pop("content"), content)
time1 = res.pop("time")
tc.assertLessEqual(time1, sendtime+5)
tc.assertGreaterEqual(time1, sendtime-5)
tc.assertDictEqual(res, {"status": "ok", "method": "chat", "roomid": roomid2, "uid": uid2, "mtype": "text"})

## test st1 send msg to st2
content = "hi, nice to meet u"
sendtime = int(time.time())
res1 = st1.producer({"method": "chat", "roomid": roomid, \
        "uid": uid, "mtype": "text", "content": content}).comsumer()
res2 = st2.comsumer()

# st1
time1 = res1.pop("time")
tc.assertLessEqual(time1, sendtime+5)
tc.assertGreaterEqual(time1, sendtime-5)
tc.assertDictEqual(res1, {"status": "ok", "method": "chat", "uid": uid})
# st2
tc.assertEqual(res2.pop("content"), content)
time2 = res2.pop("time")
tc.assertLessEqual(time2, sendtime+5)
tc.assertGreaterEqual(time2, sendtime-5)
tc.assertDictEqual(res2, {"status": "ok", "method": "chat", "roomid": roomid, "uid": uid, "mtype": "text"})

st2.disconnect()
print("done")
