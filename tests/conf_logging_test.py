from server import Server_Utils
import pytest

def test_conf_logging():
    path_correct = "/home/wizard/Projects/Liftr/logs" 
    path_generated = Server_Utils.conf_logging() 
    assert path_correct == path_generated, "The path's should be the same"

