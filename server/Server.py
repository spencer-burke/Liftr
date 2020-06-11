import sys
import socket
import subprocess
import pytest
import logging
from Server_Utils import Server_Utils, recv_file, recv_command

'''
project: liftr
title: liftr file server
author: Spencer Burke
last-updated: 6/10/20
'''

def example_server():
    HOST = '127.0.0.1'
    PORT = 9999
    DATA_PORT = 10000
    logging.basicConfig(filename='./logs/server.log', filemode='w', format='%(filename)s - %(level    name)s - %(message)s', level=logging.DEBUG)
    command = recv_command(HOST, PORT)
    if parse_connection(command) == 0:
        if command == "store":
            recv_file("example_file.txt", HOST, DATA_PORT)   

def main():
    pass

if '__name__' == '__main__':
   pass 
