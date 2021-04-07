#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter03/tcp_sixteen.py
# Simple TCP client and server that send and receive 16 octets

import argparse, socket, glob,sys

def recvall(sock, length):
  data = b''
  while len(data) < length:
    more = sock.recv(length - len(data))
    if not more:
      raise EOFError('was expecting %d bytes but only received'
                      ' %d bytes before the socket closed'
                      % (length, len(data)))
    data += more
  return data

def server(interface, port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  sock.bind((interface, port))
  sock.listen(1)
  print('Listening at', sock.getsockname())
  while True:
    print('Waiting to accept a new connection')
    sc, sockname = sock.accept()
    
    len_msg = recvall(sc, 3)
    len_msg = int(len_msg)
    message = recvall(sc, len_msg)

    message = message.decode("utf-8").split()

    cmd = message[0]
    num_of_arg = len(message)
    
    if cmd == "ls":
      if num_of_arg > 1:
        listLS = ""
        if message[1].endswith("*"):
          listLS = message[1]
        elif message[1].endswith("/"):
          listLS = message[1]+"*"
        else:
          listLS = message[1]+"/*"
        for i in glob.glob(listLS): print(" ", i)
      else:
        for i in glob.glob("*"): print(" ", i)
    
    elif cmd == "get":
      buffer = b""
      
      with open(message[1], "rb") as file:
        buffer = file.read()
      print(" ", buffer)

      with open(message[2], "wb+") as file:
        file.write(buffer)

      print('\n  Fetch:{} size: {} lokal:{}'.format(message[1], len(buffer), message[2]))

    elif cmd == "quit":
      print("  Server shutdown...")
      sc.sendall(b'Farewell, client')
      sc.close()
      print('\n  Reply sent, socket closed')
      break


    sc.sendall(b'Farewell, client')
    sc.close()
    print('\n  Reply sent, socket closed')

def client(host, port):
  while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())

    msg = bytearray(input("> "), encoding='UTF-8')
    len_msg = b"%03d" % len(msg)
    msg = len_msg+msg
    # print("\n  client to server: ", msg, "\n\n")
    # print("\ttipe msg: ", type(msg))
    
    sock.sendall(msg)
    reply = recvall(sock, 16)
    print('The server said', repr(reply),"\n")
    sock.close()
    if(msg == b'004quit'): 
      print("Client shutdown...")
      break

if __name__ == '__main__':
  choices = {'client': client, 'server': server}
  parser = argparse.ArgumentParser(description='Send and receive over TCP')
  parser.add_argument('role', choices=choices, help='which role to play')
  parser.add_argument('host', help='interface the server listens at;'
                      ' host the client sends to')
  parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                      help='TCP port (default 1060)')
  args = parser.parse_args()
  function = choices[args.role]
  function(args.host, args.p)
