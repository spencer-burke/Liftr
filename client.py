import socket
import Parser

#clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#clientsocket.connect(('localhost',8089))
#clientsocket.send('hello')

print("beginning initialization")

stringParser = Parser()
print("parser has been initialized")

print("'liftr interface started' type:'end' to end")
input = raw_input()
while(input != 'end'):
   
    
