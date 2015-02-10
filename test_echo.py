import echo_server
import echo_client
import pytest


@pytest.fixture(scope='function')
def setup_client(request):
    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP
    )

    def closer():
        client_socket.close()
    request.addfinalizer(closer)

    return client_socket


@pytest.fixture(scope='function')
def setup_server(request):
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP
    )

    def closer():
        server_socket.close()
    request.addfinalizer(closer)

    return server_socket


# Client tests
def test_echo_client(setup_client):
    pass


def test_echo_client_send(setup_client):
    pass


def test_echo_client_receive(setup_client):
    pass


# Server tests
def test_echo_server(setup_server):
    pass


def test_echo_server_send(setup_server):
    pass


def test_echo_server_receive(setup_server):
    pass
