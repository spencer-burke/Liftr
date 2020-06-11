from server import Server_Utils 
import queue
import pytest
import threading

def client_routines():
    # run the client functionality needed to test a very primitive server
    HOST = '127.0.0.1'
    PORT = 9999
    DATA_PORT = 10000

    Server_Utils.send_command("store", HOST, PORT)
    Server_Utils.store_file("./fixtures/text-file.txt", HOST, DATA_PORT)

def cleanup():
    # cleanup residual files to keep the test directory clean
    pass

def client_server_routines():
    thread_server = threading.Thread(target=Server_Utils.example_server)
    

def test_basic_server():
    thread_server = threading.Thread(target=Server_Utils.example_server)
   
'''
THIS IS NOT COMPLETE THE TEST IS STILL BEING WORKED ON
'''  
