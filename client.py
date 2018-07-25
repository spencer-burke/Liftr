import sys
import socket
from parser import Parser
#clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#clientsocket.connect(('localhost',8089))
#clientsocket.send('hello')
'''
print('beginning initialization')
parserObject = Parser("liftr")
print("liftr started type:'end' to end")
input = raw_input()
while(input != 'end'):
        if(parserObject.isInDebugMode()):
                print('debug mode is activated')
        if(input == 'debug'):
                if(parserObject.isInDebugMode()):
                        print('debug deactivation detected, leaving debug mode')
                        parserObject.disableDebugMode()
                        print('debug mode deactivated')
                else:
                        print('debug activation detected, entering debug mode')
                        parserObject.enableDebugMode()
                        print('debug mode activated')
        input = raw_input()
'''
s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
port = 60000                    # Reserve a port for your service.

s.connect((host, port))
s.send("Hello server!")

with open('received_file', 'wb') as f:
    print 'file opened'
    while True:
        print('receiving data...')
        data = s.recv(1024)
        print('data=%s', (data))
        if not data:
            break
        # write data to a file
        f.write(data)

f.close()
print('Successfully get the file')
s.close()
print('connection closed')
    
            
            
           
          
   
            
        
    
