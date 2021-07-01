#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter08/queuepi.py
# Small application that uses several different message queues

import random, threading, time, zmq, sqlite3, os, sys, hashlib

start = time.time()
perulangan = input = int(input("Banyak Perulangan : ") or "1000")

def sqlGenerator(zcontext, url, url2):
    zsock = zcontext.socket(zmq.PUB)
    zsock.bind(url)

    zsock2 = zcontext.socket(zmq.PUB)
    zsock2.bind(url2)
    
    for i in range(perulangan+1):
        n1 = random.randint(1, 99000)
        n2 = random.randint(1, 1000)
        sql = "select count(*) from MOCKDATA where ID>=%s AND ID<=%s;" % (n1, n1+n2)
        h = hash(sql)
        
        kirim = h%2
        zsock2.send_string(sql)
        kirim = str(kirim)
        
        zsock.send_string(kirim)
        time.sleep(0.03)

def return_0(zcontext, in_url, out_url):
    isock = zcontext.socket(zmq.SUB)
    isock.connect(in_url)

    isock.setsockopt(zmq.SUBSCRIBE, b'0')
    
    osock = zcontext.socket(zmq.PUSH)
    osock.connect(out_url)
    while True:
        isock.recv_string()
        osock.send_string('0')

def req_service(zcontext, in_url, in_url2, pythagoras_url, out_url):
    
    isock = zcontext.socket(zmq.SUB)
    isock.connect(in_url)
    isock.setsockopt(zmq.SUBSCRIBE, b"1")
    
    isock2 = zcontext.socket(zmq.SUB)
    isock2.connect(in_url2)
    isock2.setsockopt_string(zmq.SUBSCRIBE, "select")

    psock = zcontext.socket(zmq.REQ)
    psock.connect(pythagoras_url)
    osock = zcontext.socket(zmq.PUSH)
    osock.connect(out_url)
    
    while True:
        yangDiterima = isock.recv_string()
        sqlDiterima = isock2.recv_string()
        
        psock.send_string(sqlDiterima)
        hasilQuery = psock.recv_string()

        osock.send_string(str(hasilQuery))

def sqlite_executor(zcontext, url):
    zsock = zcontext.socket(zmq.REP)
    zsock.bind(url)

    while True:
        db = sqlite3.connect("data.db")
        cur = db.cursor()
        
        query = zsock.recv_string()
        cur.execute(str(query))
        value = int(cur.fetchone()[0])

        db.close()
        zsock.send_string(str(value))

def print_all(zcontext, url, url2):
    zsock = zcontext.socket(zmq.PULL)
    zsock.bind(url)

    sqlsock = zcontext.socket(zmq.SUB)
    sqlsock.connect(url2)
    sqlsock.setsockopt_string(zmq.SUBSCRIBE, "select")

    count = total = 0

    while True:
        value = zsock.recv_string()
        query = sqlsock.recv_string()
        count += 1
        total += int(value)
        print(count ,query, "count() = ",value)
        if (count >= perulangan): 
          endtime = time.time()-start
          print("\nnum query = %d, total return value = %d" % (count, total))
          print("waktu: = ",endtime)

def start_thread(function, *args):
    thread = threading.Thread(target=function, args=args)
    thread.daemon = True  # so you can easily Ctrl-C the whole program
    thread.start()

def main(zcontext):
    pubsub = 'tcp://127.0.0.1:6700'
    reqrep = 'tcp://127.0.0.1:6701'
    pushpull = 'tcp://127.0.0.1:6702'
    pubsub2 = 'tcp://127.0.0.1:6703'
    
    start_thread(sqlGenerator, zcontext, pubsub, pubsub2)
    start_thread(return_0, zcontext, pubsub, pushpull)
    start_thread(req_service, zcontext, pubsub, pubsub2, reqrep, pushpull)
    start_thread(sqlite_executor, zcontext, reqrep)
    start_thread(print_all, zcontext, pushpull, pubsub2)
    time.sleep(80)

if __name__ == '__main__':
    main(zmq.Context())
