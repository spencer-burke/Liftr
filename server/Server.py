import socket
import subprocess
import logging
import asyncio
import ServerUtils
import time
'''
project: liftr
title: liftr file server
author: Spencer Burke
last-updated: 6/15/20
'''

COM_PORT = 8888
DATA_PORT = 8889
# this port exists because it is required for localhost development
LOCAL_PORT = 8880

async def transfer_file(reader, writer, filename):
   with open(filename, 'rb') as reader_file:
        file_data = reader_file.read()

        writer.write(file_data)
        await writer.drain() 
        writer.write_eof()

async def transfer_data(reader, writer, data):
    writer.write(data.encode())
    await writer.drain()
    writer.write_eof()

# this needs to be modified being the server is still only being developed on localhost
async def read_file_name(addr):
    '''
    addr(tuple): tuple containing ip and port from previous connection
    '''
    time.sleep(.5)
    writer_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    writer_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    writer_sock.bind(('127.0.0.1', 8880))
    writer_sock.connect(('127.0.0.1', 8889))

    n_reader, n_writer = await asyncio.open_connection(sock=writer_sock)

    file_name = await n_reader.read()
    writer_sock.close()
    return file_name.decode()
 
async def read_file_data(addr, file_name):
    '''
    addr(tuple): tuple containing ip and port from previous connection
    file_name(string): the name of the file being connected
    '''
    time.sleep(.5)
    writer_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    writer_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    writer_sock.bind(('127.0.0.1', 8880))
    writer_sock.connect(('127.0.0.1', 8889))

    n_reader, n_writer = await asyncio.open_connection(sock=writer_sock)

    with open(file_name, 'wb') as file_writer:
        file_data = await n_reader.read()
        file_writer.write(file_data)  

    writer_sock.close()

async def get_file(addr):
    time.sleep(.5)
    # create the socket used to manage the connections to the client
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as data_sock:
        data_sock.bind(('127.0.0.1', LOCAL_PORT)) 
        # connect the first time to get the name of the file
        data_sock.connect(('127.0.0.1', DATA_PORT))
        
        # open asynchronous connection using raw connection
        n_reader, n_writer = await asyncio.open_connection(sock=data_sock)
        
        # read file name from network
        file_name = await n_reader.read()
        # send acknowledgement
        await transfer_data(n_reader, n_writer, "ack")
        #n_writer.close()
        #await n_writer.wait_closed()

        d_reader, d_writer = await asyncio.open_connection(sock=data_sock)
        
        file_data = await d_reader.read()
        print(d_reader.at_eof())
        print("got data")
        print(file_data)
        with open(file_name.decode(), 'w') as file_writer:
            file_writer.write(file_data)
        print("successfully recieved and created file") 
 
async def handle_connection(c_reader, c_writer):
    commands = ["store", "recv", "show", "ack"]

    # listen for connection and log ip from connection
    data = await c_reader.read()
    message = data.decode()
    addr = c_writer.get_extra_info('peername')
    new_addr = ('127.0.0.1', 8889)
 
    #recieve valid command
    if message == commands[0]:
        # acknowledge it
        await transfer_data(c_reader, c_writer, commands[3])
        print("acknowledgment sent")
        #read file name
        file_name = await read_file_name(addr)
        #read file data
        await read_file_data(addr, file_name)
    elif message == commands[1]:
        pass
    elif message == commands[2]:
        pass
    else:
        pass

async def main():
    server = await asyncio.start_server(handle_connection, '127.0.0.1', 8888)
    
    async with server:
        await server.serve_forever()

asyncio.run(main())     

