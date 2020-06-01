import sys
import socket
import subprocess
'''
project: liftr
title: liftr file server
author: Spencer Burke
last-updated: 6/1/20
'''
class ServerUtils:
    CHUNK_SIZE = 8 * 1024
    command_list = ["send","show","recv"]
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.configureFirewall()
        self.configureSocket(self.listener_socket)
    #configures firewall for the server to function
    #opens an incoming connection on tcp port 9999 with an iptables subrocess
    def configureFirewall(self):
        try:
            print('Configuring network firewall')
            subprocess.Popen(['iptables', '-I', 'INPUT', '-p', 'tcp', '--dport', '9999', '-j', 'ACCEPT'])
            print('Successfully configured network firewall')
        except OSError as error:
            print(str(error))
    #reconfigures the firewall
    #closes the incoming connection on tcp port 9999 with an iptables subrocess
    def closeServer(self):
        try:
            print('Shutting down server')
            subprocess.Popen(['iptables', '-D', 'INPUT', '-p', 'tcp', '--dport', '9999', '-j', 'ACCEPT'])
        except OSError as error:
            print(str(error))
    #binds socket to host
    def configureSocket(self,arg_socket):
        try:
            print('binding socket to port')
            self.listener_socket.bind((self.address, self.port))
            print('socket has been successfully bound to port')
        except socket.error as error:
            print('error binding socket to port')
            print(str(error))
        print('telling socket to listen')
        self.listener_socket.listen(5)
    #collects commands from the client for the server
    def getInfo(self):
        print('listening for information')
        client_socket, addr = self.listener_socket.accept()
        data = client_socket.recv(2048)
        return data.decode()
    #routine to send a file
    def sendFile(self, fileName):
        print('sending file')
        while True:
            client_socket, addr = self.listener_socket.accept()
            with open(fileName,'rb') as file:
                client_socket.sendfile(file, 0)
            client_socket.close()
        print('file transfer complete')
    #recieves the file
    def recieveFile(self):
        chunk = self.listener_socket.recv(CHUNK_SIZE)
        while chunk:
            chunk = self.listener_socket.recv(CHUNK_SIZE)
    #sends the command the client wishes to execute
    def sendCommand(self, command):
        try:
            print("sending current command")
            self.listener_socket.send(str.encode(command))
        except OSError as error:
            print(str(error))
