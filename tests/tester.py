#not much to see here
import socket
import os

HOST = '127.0.0.1'  
PORT = 9999       

'''
same as above but with abstractions
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

#store_file('example_text_file.txt', HOST, PORT)
#send_command("store", HOST, PORT) 
 
