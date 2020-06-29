'''
CURRENTLY WORKING REFACTORING THE SERVER INTO A NETWORKED VERSION
CURRENTLY WORKING ON LINE 46; GETTING PREVIOUS IP AND MAKING A NEW USING THE DATA_PORT
'''
import socket
import logging
import asyncio
import time
import os

'''
project: liftr
title: liftr file server
author: Spencer Burke
last-updated: 6/28/20
'''

COM_PORT = 8888
DATA_PORT = 8889
IP = conf_ip("../conf/conf.txt") 

def conf_ip(path):
    '''
    path(string): path to conf file
    return(int): the ip used for the server 
    '''
    with open(path, 'r') as reader:
        return reader.readlines()[0][4:-1]

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
    prev_ip = addr(0)
    
    time.sleep(.5)
    writer_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    writer_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    writer_sock.bind((IP, DATA_PORT))
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

def get_file_path(file_name):
    '''
    file_name(string): the name of the file to be searched for
    return(string): the path to the file within the files directory 
    '''
    return "../files/" + file_name

async def send_file_data(addr, file_name):
    '''
    addr(tuple): contains the ip and socket representing connection
    file_name(string): the name of the file being sent
    ''' 
    time.sleep(.5)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('127.0.0.1', LOCAL_PORT))
        sock.connect(('127.0.0.1', 8889))
        
        reader, writer = await asyncio.open_connection(sock=sock)

        with open(get_file_path(file_name), 'rb') as reader:
            data = reader.read()
            writer.write(data)
            await writer.drain()
            writer.write_eof()

async def send_file_presence(addr, presence):
    '''
    addr(tuple): contains the ip and socket representing connection
    presence(string): the response saying whether the file is there
    '''
    time.sleep(.5)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('127.0.0.1', LOCAL_PORT))
        sock.connect(('127.0.0.1', 8889))

        reader, writer = await asyncio.open_connection(sock=sock)
 
        await transfer_data(reader, writer, presence)

def build_string():
    '''
    return(string): string representation of all the files within the storage system
    '''
    path = "../files"
    dir_list = os.listdir(path)
    result = ""

    for _ in dir_list:
        result += _ + "\n"

    return result

async def show():
    time.sleep(.5)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('127.0.0.1', LOCAL_PORT))
        sock.connect(('127.0.0.1', 8889))

        reader, writer = await asyncio.open_connection(sock=sock)
 
        await transfer_data(reader, writer, build_string())
     
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
        await transfer_data(c_reader, c_writer, responses[0])
        # get the file name from the client
        file_name = await read_file_name(addr)
        # tell the client if the file is within the server
        if has_file(file_name):
            await send_file_presence(addr, responses[2])
            # connect to client and send the file data
            await send_file_data(addr, file_name) 
        else:
            await send_file_presence(responses[1])
    elif message == commands[2]:
        await transfer_data(c_reader, c_writer, responses[0])
        await show()    
    
def main():
    event_loop = asyncio.get_event_loop()
    protocol_factory = asyncio.start_server(handle_connection, '127.0.0.1', 8888)
    server_endpoint = event_loop.run_until_complete(protocol_factory)

    try:
        event_loop.run_forever()     
    except(KeyboardInterrupt):
            pass
    finally:
        server_endpoint.close()
        event_loop.run_until_complete(server_endpoint.wait_closed())
        event_loop.close()

if __name__ == '__main__':
     main()   

'''
    Current:
        - implement remote versions
'''
