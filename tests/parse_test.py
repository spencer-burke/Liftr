from server import Server_Utils 
import queue
import pytest
import threading

def test_parse():
    HOST = '127.0.0.1'
    PORT = 9999

    que = queue.Queue()

    server_thread = threading.Thread(target=lambda q, arg1, arg2: q.put( Server_Utils.parse_connection( Server_Utils.recv_command(arg1, arg2) ) ), args=(que, HOST, PORT))
    server_thread.start()

    client_thread = threading.Thread(target=Server_Utils.send_command, args=("store", HOST, PORT))
    client_thread.start()

    server_thread.join()
    client_thread.join() 

    result = que.get()
    assert result == 0, "return code should be 1"

