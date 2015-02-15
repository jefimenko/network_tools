import echo_server
import echo_client
import pytest
import socket
import threading


@pytest.fixture(scope='function')
def setup_client(request):
    client_socket = echo_client.create_client_socket()

    def closer():
        client_socket.close()
    request.addfinalizer(closer)

    return client_socket


@pytest.fixture(scope='function')
def setup_server(request):
    server_socket = echo_server.create_server_socket()

    def closer():
        server_socket.close()
    request.addfinalizer(closer)

    return server_socket


# Client tests
def test_echo_client(setup_client):
    assert setup_client


def test_echo_client_send_and_recieve(setup_client, setup_server):
    # Use threading to allow server to wait for connection while the
    # rest of the test function runs.
    buffsize = 8
    t = threading.Thread(target=listener, args=(setup_server, buffsize,))
    t.start()

    echo_client.comm(setup_client, 'a message')
    message_from_server = echo_client.receive(setup_client)

    assert 'a message' == message_from_server


def listener(setup_server, buffsize):
    conn, addr, message = echo_server.receive_msg(
        setup_server, buffsize)
    conn.sendall(message)
    conn.close()


# Server tests
def test_echo_server(setup_server):
    assert setup_server
    assert isinstance(setup_server, type(socket.socket()))
