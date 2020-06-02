import sys
import socket
import subprocess
import socketserver
import pytest
from Server_Utils import Server_Utils

'''
project: liftr
title: liftr file server
author: Spencer Burke
last-updated: 6/1/20
'''

#test class based main
def main():
    server_core = Server_Utils('192.168.1.109',9999)
    while True:
        data = server_core.get_info()
        print(data)

if __name__ == '__main__':
    main()

