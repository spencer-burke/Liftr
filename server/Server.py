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

async def read_file_name(addr):
    '''
    addr(tuple): tuple containing ip and port from previous connection
    '''
    time.sleep(.5)
    writer_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    writer_sock.bind(('127.0.0.1', 8880))
    writer_sock.connect(('127.0.0.1', 8889))

    n_reader, n_writer = await asyncio.open_connection(sock=writer_sock)

    file_name = await n_reader.read()
    writer_sock.close()
    return file_name.decode()
 
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
        # open connection to read file name
        file_name = await read_file_name(addr)
        #time.sleep(1)
        ##writer_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ##writer_sock.bind(('127.0.0.1', 8880))
        ##writer_sock.connect(('127.0.0.1', 8889))
        ##n_reader, n_writer = await asyncio.open_connection(sock=writer_sock)
        # open connection to read file data
 
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

