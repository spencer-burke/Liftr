import socket
import subprocess
import logging
import asyncio
import ServerUtils
import time
import os
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

def has_file(file_name):
    '''
    file_name(string): the name of the file to be searched for
    return(boolean): true if the file exists, false if it doesn't
    '''
    path = "../files/" + file_name
    exists = os.path.isfile(path)
    return exists

async def send_file_data(addr, file_name):
    '''
    addr(tuple): contains the ip and socket representing connection
    file_name(string): the name of the file being sent
    ''' 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('127.0.0.1', LOCAL_PORT))
        sock.connect(addr)
        
        reader, writer = await asyncio.open_connection(sock=addr[1])

        with open(file_name, 'rb') as reader:
            data = reader.read()
            writer.write(data)
            await writer.drain()
            writer.write_eof()

async def send_file_presence(addr, presence):
    '''
    addr(tuple): contains the ip and socket representing connection
    presence(string): the response saying whether the file is there
    '''
     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('127.0.0.1', LOCAL_PORT))
        sock.connect(addr)

        reader, writer = await asyncio.open_connection(sock=addr[1])
 
        await transfer_data(reader, writer, presence)

async def handle_connection(c_reader, c_writer):
    commands = ["store", "recv", "show"]
    responses = ["ack", "nul", "prs"]

    # listen for connection and log ip from connection
    data = await c_reader.read()
    message = data.decode()
    addr = c_writer.get_extra_info('peername')
    new_addr = ('127.0.0.1', 8889)

    if message == commands[0]:
        # acknowledge it
        await transfer_data(c_reader, c_writer, responses[0])
        # read file name
        file_name = await read_file_name(addr)
        # read file data
        await read_file_data(addr, file_name)
    elif message == commands[1]:
        # send acknowledgment
        await transer_data(c_reader, c_writer, responses[0])
        # get the file name from the client
        file_name = await read_file_name(addr)
        # tell the client if the file is within the server
        if has_file(file_name):
            await send_file_presence(responses[2])     
        else:
            await send_file_presence(responses[1])
        # connect to client and send the file data
        await send_file_data(addr, file_name) 
    elif message == commands[2]:
        pass
    else:
        pass

async def main():
    server = await asyncio.start_server(handle_connection, '127.0.0.1', 8888)
    
    async with server:
        await server.serve_forever()

asyncio.run(main())     
# MAKE SURE TO MODIFY THE RUN TIME
'''
    Current:
        - build the files system(meaning the way to store and send files in the proper dir needs to happen
        - implement other commands
        - modify run time
'''
