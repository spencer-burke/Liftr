import os
import sys
import socket
from ServerUtils import ServerUtils
'''
project: liftr
title: liftr file server
author: Spencer Burke
last-updated: 9/1/18
'''
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
def main():
    sanitizedInput = cleanInput(sys.argv)
    client_core = ServerUtils('192.168.1.109', 9999)
    if(sanitizedInput[0] == 'send'):
        #client_core.sendCommand(client_core.command_list[0])
        client_core.sendFile("testFile.txt")
    elif(sanitizedInput[0] == 'show'):
        print(os.listdir("/home/davinci/liftr/files"))
    elif(sanitizedInput[0] == 'recv'):
        pass
        #client_core.sendCommand(client_core.command_list[2])
if(__name__ == "__main__"):
    main()
