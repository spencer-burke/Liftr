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
    logging.info("Sending store command")
    Server_Utils.send_command("store", HOST, PORT)
    logging.info("Sent store command")
    logging.info("storing file on data port")
    Server_Utils.store_file("./fixtures/text-file.txt", HOST, DATA_PORT)
    logging.info("successfully stored file on data port")

def server_routines():
    # very primitive server
    logging.info("Started mock server")
    HOST = '127.0.0.1'
    PORT = 9999
    DATA_PORT = 10000
    logging.info("listening on port 9999")
    command = Server_Utils.recv_command(HOST, PORT)
    logging.info("successfully recieved command")
    if Server_Utils.parse_connection(command) == 0:
        logging.info("successfully parsed incoming connection")
        if command == "store":
            Server_Utils.recv_file("example_file.txt", HOST, DATA_PORT)   

def client_server_routines():
    thread_server = threading.Thread(target=server_routines)
    thread_server.start()

    thread_client = threading.Thread(target=client_routines)
    thread_client.start()

    thread_server.join()
    thread_client.join()

def cleanup():
    # cleanup residual files to keep the test directory clean
    pass

def test_basic_server():
    path = Server_Utils.conf_logging() + 'server.log'
    logging.basicConfig(filename=path, filemode='w', format='%(filename)s - %(level    name)s - %(message)s', level=logging.DEBUG)
    client_server_routines() 
    assert os.path.isfile("example_file.txt") == True
    cleanup() 

client_server_routines()
'''
THIS IS NOT COMPLETE THE TEST IS STILL BEING WORKED ON
'''  
