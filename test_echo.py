import echo_server
import echo_client
import pytest
import socket


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


def test_echo_client_send(setup_client):
    pass

def test_echo_client_receive(setup_client):
    pass


# Server tests
def test_echo_server(setup_server):
    assert setup_server


def test_echo_server_send(setup_server):
    pass


def test_echo_server_receive(setup_server):
    pass
