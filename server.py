import socket
#reserve a port for the service
port = 60000
#create a socket object
sock = socket.socket()
#get the local machine name
host = sock.gethostname()
#bind to the port
sock.bind((host,port))
#wiat for client connection
sock.listen(5)
print("----Server Listening----")
while True:
    #establish connection with client
    conn, addr = sock.accept()
    print("Connection incoming from ", addr)
    #the file
    filename='testfile.txt'
    f = open(filename, 'rb')
    l = f.read(1024)
    while (l):
        conn.send(l)
        print('File sent', repr(l))
        l = f.read(1024)
    f.close()
    print('Finished file transfer')
    conn.send('Connection complete')
    conn.close()
