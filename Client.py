import os
import sys
import socket
from ServerUtils import ServerUtils
#cleans the input of the name of the program
def cleanInput(list_arg):
        result = []
        i = 0
        while i < len(sys.argv):
                if i > 0:
                        result.append(sys.argv[i])
                i+=1
        return result
#main function for the client program
def main()
    sanitizedInput = cleanInput(sys.argv)
    client_core = ServerUtils('192.168.109', 9999)    
    if(sanitizedInput[0] == 'send'):
       client_core.sendFile()
    elif(sanitizedInput[0] == 'show'):
        
    elif(sanitizedInput[0] == 'recv'):
        

if(__name__ == "__main__"):
    main()