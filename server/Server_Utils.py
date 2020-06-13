import socket
import subprocess
import logging
import os

'''
project: liftr
title: liftr file server
author: Spencer Burke
last-updated: 6/12/20
'''

''' 
THESE ABSTRACTIONS ARE NOT YET COMPLETE THEY MIGHT BE REAFCTORED INTO A CLASS
THE CONSTANT BIND AND CONFIGURE CALLS MIGHT ALSO BE REMOVED
'''

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
    logging.info("Successfully received" + new_command)
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
    
def conf_logging():
    '''
    path(String): the appropriate path the log file with the project directory
    '''
    #logging.basicConfig(filename='../logs/server.log', filemode='w', format='%(filename)s - %(levelname)s - %(message)s', level=logging.INFO)
    path = os.getcwd()
    index = path.index("Liftr")
    path_project = path[0:index+5]
    path_log_result = path_project + "/logs" 
    return path_log_result

def configure_firewall():
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
    
    def close_server():
        '''
        reconfigures the firewall
        closes the incoming connection on tcp port 9999 with an iptables subrocess
        '''
        try:
            logging.info('Shutting down server')
            subprocess.Popen(['iptables', '-D', 'INPUT', '-p', 'tcp', '--dport', '9999', '-j', 'ACCEPT'])
        except OSError as error:
            logging.error(str(error))

'''
use asyncio for the server
'''
