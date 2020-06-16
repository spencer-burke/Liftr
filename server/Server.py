import socket
import subprocess
import logging
import asyncio
import ServerUtils

'''
project: liftr
title: liftr file server
author: Spencer Burke
last-updated: 6/15/20
'''

async def transfer_file(reader, writer, filename):
   with open(filename, 'rb') as reader_file:
        file_data = reader_file.read()

        writer.write(file_data)
        await writer.drain() 

async def transfer_command(reader, writer, command):
    writer.write(command.encode())
    await writer.drain()
 
async def handle_connection(reader, writer):
    commands = ["store", "recv", "show", "ack"]

    data = await reader.read(100)
    message = data.decode()

    if message == commands[0]:
        pass
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
