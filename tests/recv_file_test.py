from server import Server_Utils 
import pytest
import threading
import os

def run_server_routines():
    #using threads to test the server 
    HOST = '127.0.0.1'
    PORT = 9999

    file_name_recv = 'recv-file.txt'
    file_name = './fixtures/text-file.txt'

    thread_server = threading.Thread(target=Server_Utils.recv_file, args=(file_name_recv, HOST, PORT))
    thread_server.start()

    thread_client = threading.Thread(target=Server_Utils.store_file, args=(file_name, HOST, PORT))
    thread_client.start()

    thread_server.join()
    thread_client.join()

def test_store_file():
    run_server_routines()
    assert os.path.isfile('./recv-file.txt') == True, "File should exist"

def main():
    test_store_file()

def cleanup():
    #cleans up after the test to make sure the directory is only filled with test files
    os.remove('recv-file.txt')
 
if __name__ == '__main__':
    main()
    cleanup()

'''
Currently working on building fixtures into the tests to clean up the directory 
'''
