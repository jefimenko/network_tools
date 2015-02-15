from echo_server\
    import create_server_socket, response_ok, response_error, \
    parse_request, main
import echo_client
import pytest
import threading
import socket


def test_ok():
    assert response_ok() == """\
HTTP/1.1 200 OK\r\n\
"""


def test_error():
    assert """\
HTTP/1.1 403 Forbidden\r\n\
""" == response_error(ValueError('403', "Forbidden"))


def test_parse():
    # Working case
    test_string = """\
GET some_uri HTTP/1.1\r\n\
some head\r\n\
\r\n\
some body\r\n\
\r\n\
some footer\
"""
    assert parse_request(test_string)[0] == "some_uri"
    # Bad protocol case
    with pytest.raises(ValueError):
        parse_request("POST asdf HTTP/1.1")
    # Non-GET case
    with pytest.raises(ValueError):
        parse_request("GET asdf HTTP/1.0")
    # Something that's not even a request.
    with pytest.raises(ValueError):
        parse_request('just wrong')


# Functional tests
# run echo_server

@pytest.fixture(scope="function")
def server_starter(request):
    # Create an flag to end the thread with
    event = threading.Event()
    event.set()

    # run echo server_start
    t = threading.Thread(target=main, args=(event,))
    t.start()

    return event


def test_interaction():
    event = threading.Event()
    event.set()

    # run echo server_start
    t = threading.Thread(target=main, args=(event,))
    t.start()

    # Expected
    client_socket = echo_client.create_client_socket()
    client_socket.connect(('127.0.0.1', 50000))
    client_socket.sendall('GET something HTTP/1.1\r\n')
    client_socket.shutdown(socket.SHUT_WR)
    assert echo_client.receive(client_socket) == """\
HTTP/1.1 200 OK\r\n\
"""
    client_socket.close()

    # Wrong method
    client_socket = echo_client.create_client_socket()
    client_socket.connect(('127.0.0.1', 50000))
    client_socket.sendall('POST something HTTP/1.1\r\n')
    client_socket.shutdown(socket.SHUT_WR)
    assert echo_client.receive(client_socket) == """\
HTTP/1.1 403 Forbidden\r\n\
"""
    client_socket.close()

    # Wrong method and wrong protocol
    client_socket = echo_client.create_client_socket()
    client_socket.connect(('127.0.0.1', 50000))
    client_socket.sendall('POST something HTTP/1.0\r\n')
    client_socket.shutdown(socket.SHUT_WR)
    assert echo_client.receive(client_socket) == """\
HTTP/1.1 403 Forbidden\r\n\
"""
    client_socket.close()

    # Wrong protocol
    client_socket = echo_client.create_client_socket()
    client_socket.connect(('127.0.0.1', 50000))
    client_socket.sendall('GET something HTTP/1.0\r\n')
    client_socket.shutdown(socket.SHUT_WR)
    assert echo_client.receive(client_socket) == """\
HTTP/1.1 403 Forbidden\r\n\
"""
    client_socket.close()

    # Missing information
    client_socket = echo_client.create_client_socket()
    client_socket.connect(('127.0.0.1', 50000))
    client_socket.sendall('GET something\r\n')
    client_socket.shutdown(socket.SHUT_WR)
    assert echo_client.receive(client_socket) == """\
HTTP/1.1 400 Bad Request\r\n\
"""
    client_socket.close()

    client_socket = echo_client.create_client_socket()
    client_socket.connect(('127.0.0.1', 50000))
    client_socket.sendall('something HTTP/1.0\r\n')
    client_socket.shutdown(socket.SHUT_WR)
    assert echo_client.receive(client_socket) == """\
HTTP/1.1 400 Bad Request\r\n\
"""
    client_socket.close()

    client_socket = echo_client.create_client_socket()
    client_socket.connect(('127.0.0.1', 50000))
    client_socket.sendall('hello')
    client_socket.shutdown(socket.SHUT_WR)
    assert echo_client.receive(client_socket) == """\
HTTP/1.1 400 Bad Request\r\n\
"""
    client_socket.close()

    print even.isSet()
    event.clear()
    print event.isSet()
    # Force .accept() to return.
    socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP).connect(('127.0.0.1', 50000))
    print 'checkcheck'
