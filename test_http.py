from echo_server\
    import create_server_socket, response_ok, response_error, parse_request
import pytest


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
