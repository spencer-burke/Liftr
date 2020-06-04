import socket
import subprocess
import logging

'''
project: liftr
title: liftr file server
author: Spencer Burke
last-updated: 6/1/20
'''

class Server_Utils:
    CHUNK_SIZE = 8 * 1024
    command_list = ["send","show","recv"]
    logging.basicConfig(filename='./Logs/server.log', filemode='w', format='%(filename)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.configure_firewall()
        self.configure_socket(self.listener_socket)

    def configure_firewall(self):
        '''
        configures firewall for the server to function
        opens an incoming connection on tcp port 9999 with an iptables subrocess    
        '''
        try:
            logging.info('Configuring network firewall')
            subprocess.Popen(['iptables', '-I', 'INPUT', '-p', 'tcp', '--dport', '9999', '-j', 'ACCEPT'])
            print('Successfully configured network firewall')
            logging.info('Successfully configured network firewall')
        except OSError as error:
            logging.error(str(error)) 
    
    def close_server(self):
        '''
        reconfigures the firewall
        closes the incoming connection on tcp port 9999 with an iptables subrocess
        '''
        try:
            logging.info('Shutting down server')
            subprocess.Popen(['iptables', '-D', 'INPUT', '-p', 'tcp', '--dport', '9999', '-j', 'ACCEPT'])
        except OSError as error:
            logging.error(str(error))

    def configure_socket(self,arg_socket):
        #binds socket to host
        try:
            logging.info('binding socket to port')
            self.listener_socket.bind((self.address, self.port))
            logging.info('socket has been successfully bound to port')
            print('telling socket to listen')
            self.listener_socket.listen(5)           
        except socket.error as error:
            logging.error(str(error))

    def get_info(self):
        #collects commands from the client for the server
        logging.info('listening for information')
        client_socket, addr = self.listener_socket.accept()
        data = client_socket.recv(2048)
        return data.decode()

    def send_file(self, fileName):
        #routine to send a file
        logging.info('sending file')
        while True:
            client_socket, addr = self.listener_socket.accept()
            with open(fileName,'rb') as file:
                client_socket.sendfile(file, 0)
            client_socket.close()
            logging.info('file transfer complete')

    def recieve_file(self):
        #recieves the file
        chunk = self.listener_socket.recv(CHUNK_SIZE)
        while chunk:
            chunk = self.listener_socket.recv(CHUNK_SIZE)

    def send_command(self, command):
        #sends the command the client wishes to execute
        try:
            logging.info("sending current command")
            self.listener_socket.send(str.encode(command))
        except OSError as error:
            logging.error(str(error))

