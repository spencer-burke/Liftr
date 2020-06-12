from server import Server 
from server import Server_Utils
import queue
import pytest
import threading
import os
import logging

def client_routines():
    # run the client functionality needed to test a very primitive server
    HOST = '127.0.0.1'
    PORT = 9999
    DATA_PORT = 10000

    Server_Utils.send_command("store", HOST, PORT)
    logging.info("Sending store command")
    Server_Utils.store_file("./fixtures/text-file.txt", HOST, DATA_PORT)
    logging.info("storing file on data port")

def client_server_routines():
    thread_server = threading.Thread(target=Server.example_server)
    thread_server.start()

    thread_client = threading.Thread(target=client_routines)
    thread_client.start()

    thread_server.join()
    thread_client.join()

def cleanup():
    # cleanup residual files to keep the test directory clean
    pass

def test_basic_server():
    client_server_routines() 
    assert os.path.isfile("text-file.txt") == True
    cleanup() 
'''
THIS IS NOT COMPLETE THE TEST IS STILL BEING WORKED ON
'''  
