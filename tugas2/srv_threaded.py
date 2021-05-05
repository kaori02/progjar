#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter07/srv_threaded.py
# Using multiple threads to serve several clients in parallel.

from tugas2.klien_paralel import recvall
import zen_utils
from threading import Thread
import sys


value = 0


def start_threads(listener, workers=4):
    t = (listener,)
    for i in range(workers):
        Thread(target=custom_thread, args=t).start()

def custom_thread(listener):
    while 1:
        sock, address = listener.accept()
        print('Menerima koneksi dari: {}'.format(address))
        try:
            while 1:
                custom_handle_request(sock)
        except EOFError:
            print('Socket Klien ke  {} telat ditutup'.format(address))
        except Exception as e:
            print('Klien {} error: {}'.format(address,e))
        finally:
            sock.close()

def custom_handle_request(sock):
    # mirip seperti sequential.py & klien_paralel.py

    global value
    # global value karna ini nilai yang akan diupdate oleh worker

    len_msg = recvall(sock, 3)
    message = recvall(sock, int(len_msg))
    message = str(message, encoding="ascii")
    # kenapa di encoding? karna untung pengiriman data string ke bentuk byte

    ii = message.split()
    if ii[0]=="ADD":
        value += int(ii[1])
    elif ii[0]=="DEC":
        value -= int(ii[1])
    else:
        print("unknown command...: ", ii)
        sys.exit(0)

    new_msg = "value : " + str(value)
    len_msg = b"%03d" % (len(new_msg),)
    new_msg = len_msg + bytes(new_msg, encoding="ascii")
    sock.sendall(new_msg)


if __name__ == '__main__':
    address = zen_utils.parse_command_line('multi-threaded server')
    listener = zen_utils.create_srv_socket(address)
    start_threads(listener)
