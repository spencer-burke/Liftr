import sys
import socket
import subprocess

'''
project: liftr
title: liftr file server
author: Spencer Burke
last-updated: 6/1/20
'''

class Server_Utils:
    CHUNK_SIZE = 8 * 1024
    command_list = ["send","show","recv"]

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.configureFirewall()
        self.configureSocket(self.listener_socket)

    def configure_firewall(self):
        '''
        configures firewall for the server to function
        opens an incoming connection on tcp port 9999 with an iptables subrocess    
        '''
        try:
            print('Configuring network firewall')
            subprocess.Popen(['iptables', '-I', 'INPUT', '-p', 'tcp', '--dport', '9999', '-j', 'ACCEPT'])
            print('Successfully configured network firewall')
        except OSError as error:
            print(str(error))
    
    def close_server(self):
        '''
        reconfigures the firewall
        closes the incoming connection on tcp port 9999 with an iptables subrocess
        '''
        try:
            print('Shutting down server')
            subprocess.Popen(['iptables', '-D', 'INPUT', '-p', 'tcp', '--dport', '9999', '-j', 'ACCEPT'])
        except OSError as error:
            print(str(error))

    def configure_socket(self,arg_socket):
        #binds socket to host
        try:
            print('binding socket to port')
            self.listener_socket.bind((self.address, self.port))
            print('socket has been successfully bound to port')
        except socket.error as error:
            print('error binding socket to port')
            print(str(error))
        print('telling socket to listen')
        self.listener_socket.listen(5)

    def get_info(self):
        #collects commands from the client for the server
        print('listening for information')
        client_socket, addr = self.listener_socket.accept()
        data = client_socket.recv(2048)
        return data.decode()

    def send_file(self, fileName):
        #routine to send a file
        print('sending file')
        while True:
            client_socket, addr = self.listener_socket.accept()
            with open(fileName,'rb') as file:
                client_socket.sendfile(file, 0)
            client_socket.close()
        print('file transfer complete')

    def recieve_file(self):
        #recieves the file
        chunk = self.listener_socket.recv(CHUNK_SIZE)
        while chunk:
            chunk = self.listener_socket.recv(CHUNK_SIZE)

    def send_command(self, command):
        #sends the command the client wishes to execute
        try:
            print("sending current command")
            self.listener_socket.send(str.encode(command))
        except OSError as error:
            print(str(error))

