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
    
    len_msg = recvall(sc, 5)
    len_msg = int(len_msg)
    message = recvall(sc, len_msg)

    message = message.decode("utf-8").split()

    cmd = message[0]
    num_of_arg = len(message)

    back_message = ""
    
    if cmd == "ls":
      if num_of_arg > 1:
        listLS = ""
        if message[1].endswith("*"):
          listLS = message[1]
        elif message[1].endswith("/"):
          listLS = message[1]+"*"
        else:
          listLS = message[1]+"/*"
        for i in glob.glob(listLS):
          back_message = back_message + i + " "
      else:
        for i in glob.glob("*"):
          back_message = back_message + i + " "
    
    elif cmd == "get":
      buffer = b""
      
      with open(message[1], "rb") as file:
        buffer = file.read()

      with open(message[2], "wb+") as file:
        file.write(buffer)

      back_message = '\n  Fetch:{} size: {} lokal:{}'.format(message[1], len(buffer), message[2])
      
    elif cmd == "quit":
      back_message = "Server shutdown..."
      print("  Server shutdown...")
    
    back_message = bytearray(back_message, encoding='UTF-8')
    len_bck_msg = b"%05d" % len(back_message)
    back_message = len_bck_msg+back_message
    sc.sendall(back_message)
    sc.close()
    print('\n  Reply sent, socket closed')
    if cmd == "quit":break

def client(host, port):
  while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())

    user_input = input("> ")
    msg = bytearray(user_input, encoding='UTF-8')
    len_msg = b"%05d" % len(msg)
    msg = len_msg+msg

    user_input = user_input.split()
    
    sock.sendall(msg)
    reply = recvall(sock, 5)
    reply = int(reply)

    rep_msg = recvall(sock, reply)
    rep_msg = rep_msg.decode("utf-8").split()
    if(user_input[0] == "ls"):
      for i in rep_msg: print(i)
    else:
      print("\n"+' '.join(rep_msg))
      print("")

    sock.close()
    if(user_input[0] == 'quit'): 
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
