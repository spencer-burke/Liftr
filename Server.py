import sys
import socket
import subprocess
import pytest
from Server_Utils import Server_Utils

'''
project: liftr
title: liftr file server
author: Spencer Burke
last-updated: 6/3/20
'''

HOST = '127.0.0.1'
PORT = 9999

'''
receiving a file(this is not done it is a proof of concept and still requires things like proper dynamic file names) 
'''
#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#    sock.bind((HOST, PORT))
#    sock.listen()
#    conn, addr = sock.accept()
#    with conn:
#        new_file = open('hello_file', 'wb')
#        data = conn.recv(1)
#        new_file.write(data)
#        while data:
#            data = conn.recv(1024)
#            new_file.write(data)
#        new_file.close()
'''
receiving a command
'''
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.bind((HOST, PORT))
sock.listen()
conn, addr = sock.accept()
new_command = ""
with conn:
    data = conn.recv(1)
    new_command += data.decode("utf-8")
    while data:
        data = conn.recv(1024)
        new_command += data.decode("utf-8")
print(new_command)
sock.close()

