from echo_server import create_server_socket, response_ok, response_error, parse_request


def test_ok():
    assert response_ok() == """
        HTTP/1.1 200 OK\r\n
        Content-Type: text/plain\r\n
        \r\n
        Hey you.\r\n
    """


def test_error():
    assert response_error()


def test_parse():
    assert parse_request('hello')
