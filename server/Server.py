import socket
import logging
import asyncio
import time
import os

'''
project: liftr
title: liftr file server
author: Spencer Burke
last-updated: 6/29/20
'''

COM_PORT = 8888
DATA_PORT = 8889

def conf_ip(path):
    '''
    path(string): path to conf file
    return(int): the ip used for the server 
    '''
    with open(path, 'r') as reader:
        return reader.readlines()[0][4:-1]

IP = conf_ip("../conf/conf.txt") 

async def transfer_file(reader, writer, filename):
   with open(filename, 'rb') as reader_file:
        file_data = reader_file.read()

        writer.write(file_data)
        await writer.drain() 
        writer.write_eof()

async def transfer_data(writer, data):
    writer.write(data.encode())
    await writer.drain()
    writer.write_eof()

async def read_file_name(addr):
    '''
    addr(tuple): contains the ip and socket representing previous connection
    '''
    new_addr = (addr[0], DATA_PORT)
    
    time.sleep(.5)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((IP, DATA_PORT))
        sock.connect(new_addr)

        reader, writer = await asyncio.open_connection(sock=sock)

        file_name = await n_reader.read()
        return file_name.decode()

async def read_file_data(addr, file_name):
    '''
    addr(tuple): contains the ip and socket representing previous connection
    file_name(string): the name of the file being connected
    '''
    new_addr = (addr[0], DATA_PORT)

    time.sleep(.5)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((IP, DATA_PORT))
        sock.connect(new_addr)

        reader, writer = await asyncio.open_connection(sock=sock)

        with open(file_name, 'wb') as file_writer:
                file_data = await n_reader.read()
                file_writer.write(file_data)  

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
    addr(tuple): contains the ip and socket representing previous connection
    file_name(string): the name of the file being sent
    ''' 
    new_addr = (addr[0], DATA_PORT)

    time.sleep(.5)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((IP, DATA_PORT))
        sock.connect(new_addr)
        
        reader, writer = await asyncio.open_connection(sock=sock)

        with open(get_file_path(file_name), 'rb') as reader:
            data = reader.read()
            writer.write(data)
            await writer.drain()
            writer.write_eof()

async def send_file_presence(addr, presence):
    '''
    addr(tuple): contains the ip and socket representing previous connection
    presence(string): the response saying whether the file is there
    '''
    new_addr = (addr[0], DATA_PORT)

    time.sleep(.5)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((IP, DATA_PORT))
        sock.connect(new_addr)

        reader, writer = await asyncio.open_connection(sock=sock)
 
        await transfer_data(writer, presence)

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

async def show(addr):
    '''
    addr(tuple): contains the ip and socket representing connection    
    '''                                                                    
    new_addr = (addr[0], DATA_PORT)

    time.sleep(.5)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((IP, DATA_PORT))
        sock.connect(new_addr)

        reader, writer = await asyncio.open_connection(sock=sock)
 
        await transfer_data(writer, build_string())
     
async def handle_connection(reader, writer):
    commands = ["store", "recv", "show"]
    responses = ["ack", "nul", "prs"]

    # listen for connection and log ip from connection
    data = await reader.read()
    message = data.decode()
    addr = writer.get_extra_info('peername')

    if message == commands[0]:
        # send acknowledgment
        await transfer_data(writer, responses[0])
        # read file name
        file_name = await read_file_name(addr)
        # read file data
        await read_file_data(addr, file_name)
    elif message == commands[1]:
        # send acknowledgment
        await transfer_data(writer, responses[0])
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
        # acknowledge it
        await transfer_data(writer, responses[0])
        await show()    
    
def main():
    event_loop = asyncio.get_event_loop()
    protocol_factory = asyncio.start_server(handle_connection, IP, 8888) 
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

