import sys
import socket
import subprocess
'''
title: liftr file server
author: Spencer Burke
last-updated: 8/22/18
'''
#configures firewall for the server to function
#opens an incoming connection on tcp port 9999 with an iptables subrocess
def configureFirewall():
    try:
        print('Configuring network firewall')
        subprocess.Popen(['iptables', '-I', 'INPUT', '-p', 'tcp', '--dport', '9999', '-j', 'ACCEPT'])
        print('Successfully configured network firewall')
    except OSError as error:
        print(str(error))
#reconfigures the firewall
#closes the incoming connection on tcp port 9999 with an iptables subrocess
def closeServer():
    try:
        print('Shutting down server')
        subprocess.Popen(['iptables', '-D', 'INPUT', '-p', 'tcp', '--dport', '9999', '-j', 'ACCEPT'])
    except OSError as error:
        print(str(error))
#binds socket to host
def configureSocket(arg_socket):
    try:
        print('binding socket to port')
        arg_socket.bind(('192.168.1.109', 9999))
        print('socket has been successfully bound to port')
    except socket.error as error:
        print('error binding socket to port')
        print(str(error))
    print('telling socket to listen')
    arg_socket.listen(5)
#collects incoming information
def collectInfo(arg_socket):
    print('looking for connections')
    client_socket, addr = arg_socket.accept()
    print(str(addr))
    data = client_socket.recv(2048)
    reply = 'server output: ' + data.decode()
    print(reply)
    print('connection complete')
#routine to send a file
def sendFile(arg_socket,arg_file_name):
    print('sending file')
    while True:
        client_socket, addr = arg_socket.accept()
        with open('testFile.txt','rb') as file:
            client_socket.sendfile(file, 0)
        client_socket.close()
    print('file transfer complete')
#main function for entire server
def main():
    configureFirewall()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    configureSocket(server_socket)
    print('socket successfully listening on port 9999 with the ip address')
    front_input = input()
    #feedback loop
    while front_input != 'end':
        if front_input == 'show':
            collectInfo(server_socket)
        front_input = input()
    closeServer()
if __name__ == "__main__":
    main()
