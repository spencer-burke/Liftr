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
commands = ['send','show','recv']
if sanitizedInput[0] == 'send':
    client_socket = socket.socket()
    print('initiating the send command')
    client_socket.connect(('192.168.1.109', 9999))
    print('successfully connected')
    client_socket.send(str.encode('hello there'))
    print('successfully sent data')
    client_socket.close()
    print('script complete')
