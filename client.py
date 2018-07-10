import socket
from parser import Parser
#clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#clientsocket.connect(('localhost',8089))
#clientsocket.send('hello')
parserObject = Parser("liftr")
print("beginning initialization")
print("liftr interface started type:'end' to end")
input = raw_input()
while(input != 'end'):
        if(input == 'debug'):
                print('debug activation detected, entering debug mode')
                parserObject.enableDebugMode
        input = raw_input()
    
            
            
           
          
   
            
        
    
