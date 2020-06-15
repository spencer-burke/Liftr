import socket
import subprocess
import logging
from server import Server_Utils

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
    command = Server_Utils.recv_command(HOST, PORT)
    logging.info("listening on port 9999")
    if Server_Utils.parse_connection(command) == 0:
        if command == "store":
            Server_Utils.recv_file("example_file.txt", HOST, DATA_PORT)   

def main():
    example_server() 

if __name__ == "__main__":
    main()
