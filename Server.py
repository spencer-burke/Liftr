import sys
import socket
import subprocess
from ServerUtils import ServerUtils
'''
project: liftr
title: liftr file server
author: Spencer Burke
last-updated: 8/28/18
'''
#test class based main
def main():
    server_core = ServerUtils('192.168.1.109',9999)
    while True:
        data = server_core.getInfo()
        print(data)
if __name__ == '__main__':
    main()
