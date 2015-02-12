from echo_server import create_server_socket, response_ok, response_error, parse_request


def test_ok():
    assert response_ok() == """
        HTTP/1.1 200 OK\r\n
        Content-Type: text/plain\r\n
        \r\n
        Hey you.\r\n
    """


def test_error():
    assert response_error(404) == """
        HTTP/1.1 404\r\n
        \r\n
    """


def test_parse():
    # Working case
    test_string = """
        GET some_uri HTTP/1.1\r\n
        some head\r\n
        \r\n
        some body\r\n
    """
    assert parse_request(test_string) == "some_uri"
    # Bad protocol case

    # Non-GET case
