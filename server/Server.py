import socket
import subprocess
import logging
import asyncio
from server import Server_Utils

'''
project: liftr
title: liftr file server
author: Spencer Burke
last-updated: 6/13/20
'''

async def handle_connection(reader, writer):
    '''
    reader(asyncio.StreamReader): the object to read streams from accepted connections
    writer(asyncio.StreamWriter): the object to write streams to accepted connections
    '''
    # Read until EOF reached
    recieved_data = await reader.read()
    # Still working on all of these schemes  

