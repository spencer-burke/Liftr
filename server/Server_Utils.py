import socket
import subprocess
import logging

'''
project: liftr
title: liftr file server
author: Spencer Burke
last-updated: 6/5/20
'''

class Server_Utils:
    CHUNK_SIZE = 8 * 1024
    command_list = ["store","show","retr"]
    logging.basicConfig(filename='../logs/server.log', filemode='w', format='%(filename)s - %(levelname)s - %(message)s', level=logging.INFO)

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

def store_file(file_name, host, port):
    '''
    file_name(String): name of the file being sent
    host(string): ip address of the host being connected to
    port(int): port number being connected to on the host
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        file_data = open(file_name, 'rb')
        data = file_data.read() 
        s.connect((host, port))
        s.sendall(data)
        file_data.close()
        s.close()

''' 
THESE ABSTRACTIONS ARE NOT YET COMPLETE THEY MIGHT BE REAFCTORED INTO A CLASS
THE CONSTANT BIND AND CONFIGURE CALLS MIGHT ALSO BE REMOVED
'''
def send_command(command, host, port):
    '''
    command(string): name of the command being sent
    host(string): ip address of the host being connected to
    port(int): port number being connected to on the host
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(command.encode("utf-8"))
        s.close()

def recv_file(file_name, host, port):
    '''
    command(string): name of the command being sent
    host(string): ip address of the host being connected to    
    file_name(string): name of file to be received
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen()
        conn, addr = sock.accept()
        with conn:
            new_file = open(file_name, 'wb')
            data = conn.recv(1)
            new_file.write(data)
            while data:
                data = conn.recv(1024)
                new_file.write(data)
            new_file.close()

def recv_command(host, port):
    '''
    command(string): name of the command being sent
    host(string): ip address of the host being connected to    
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()
    conn, addr = sock.accept()
    new_command = ""
    with conn:
        data = conn.recv(1)
        new_command += data.decode("utf-8")
        while data:
            data = conn.recv(1024)
            new_command += data.decode("utf-8")
    logging.info(new_command)
    sock.close()
    return new_command

def parse_connection(command):
    '''
    command(string): the command received from the connection
    ''' 
    commands = ["store", "recv", "show"]
    if  command == commands[0]:
        return 0
    elif command  == commands[1]:
        return 0
    elif commands == commands[2]:
        return 0
    else:
        return 1
    
    
'''
curr note(the list command can be used to create a list of the bytes recieved[an ascii character code per byte]
getting the length of this list can be used to determine if the thing received is a command
add try catch blocks to the methods being methods hang in threads without them
''' 
