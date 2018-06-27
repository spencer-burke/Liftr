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
    if(input == "help"):
        print("commands:")
        print("show: shows the files inside the liftr server")
        print("send: sends current file to the liftr server, syntax --> send: filename")
        print("retrieve: gets a file in the liftr server")
    
        
    
