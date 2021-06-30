#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter08/queuepi.py
# Small application that uses several different message queues

import random, threading, time, zmq, sqlite3, os, sys, hashlib
B = 2
def sqlGenerator(zcontext, url):
    """Produce random points in the unit square."""
    zsock = zcontext.socket(zmq.PUB)
    zsock.bind(url)
    count = 0
    
    while True:
        kirim = bin(0).lstrip('0b').zfill(B)
        zsock.send_string(kirim)
        if(kirim.startswith("0")):count +=1
        print("count kirim :", count)
        time.sleep(0.1)

def return_0(zcontext, in_url, out_url):
    """Coordinates in the lower-left quadrant are inside the unit circle."""
    isock = zcontext.socket(zmq.SUB)
    isock.connect(in_url)

    isock.setsockopt(zmq.SUBSCRIBE, b'0')
    
    osock = zcontext.socket(zmq.PUSH)
    osock.connect(out_url)
    count = 0
    while True:
        isock.recv_string()
        count += 1
        # print("\nreturn 0 terima :" ,isock.recv_string())
        print("\nreturn 0 count :" ,count)
        osock.send_string('0')

def start_thread(function, *args):
    thread = threading.Thread(target=function, args=args)
    thread.daemon = True  # so you can easily Ctrl-C the whole program
    thread.start()

def main(zcontext):
    pubsub =    'tcp://127.0.0.1:6700'
    reqrep =    'tcp://127.0.0.1:6701'
    pushpull =  'tcp://127.0.0.1:6702'
    
    start_thread(sqlGenerator, zcontext, pubsub)
    start_thread(return_0, zcontext, pubsub, pushpull)
    time.sleep(5)

if __name__ == '__main__':
    main(zmq.Context())
