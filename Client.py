import os
import sys
import socket
#cleans the input of the name of the program
def cleanInput(list_arg):
        result = []
        i = 0
        while i < len(sys.argv):
                if i > 0:
                        result.append(sys.argv[i])
                i+=1
        return result
sanitizedInput = cleanInput(sys.argv)
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
#recieves the file
def receive():
    client_socket = socket.socket()
    configure_socket(client_socket)
if(sanitizedInput[0] == 'send'):
    client_socket = socket.socket()
    client_socket.connect(('192.168.1.109', 9999))
    client_socket.send(str.encode('send'))
    client_socket.close()
elif(sanitizedInput[0] == 'show'):
    client_socket = socket.socket()
    client_socket.connect(('192.168.1.109', 9999))
    client_socket.send(str.encode('show'))
    client_socket.close()
elif(sanitizedInput[0] == 'recv'):
    client_socket = socket.socket()
    client_socket.connect(('192.168.1.109', 9999))
    client_socket.send(str.encode('recv'))
    client_socket.close()
