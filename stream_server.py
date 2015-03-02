import gevent
from gevent import socket
from gevent import  monkey; monkey.patch_socket()

from echo_server import receive_msg, resolve_uri, response_ok, response_error, parse_request

from threading import Event
import time


def create_socket(port):
    """
    Return a socket with a, limited, variable IP address
    """
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)
    # Set up the server socket
    server_socket.bind(('127.0.0.1', 50000 + port))
    server_socket.listen(1)
    return server_socket


def main(socket):
    buffsize = 64

    server_socket = socket

    conn, addr, message = receive_msg(server_socket, buffsize)

    # Cut up message
    message = message.split('\r\n\r\n')
    try:
        # All assignments up until a line that causes an exception
        # persist. Only bind symbols to parts of the request that
        # exist.
        header = message[0]
        body = message[1]
        footer = message[2]
    except IndexError:
        pass

    try:
        # Parse request
        uri = parse_request(header)
        content_type, body = resolve_uri(uri)
        formed_response = response_ok(content_type, body)
        # Send the appropriate message
        # OK
    except ValueError as e:
        # Errors
        print e[0]
        print e[1]
        print type(e)
        formed_response = response_error(e)
    except UnboundLocalError as e:
        # Close the connection and server and break out of the loop
        # trying to send anything.
        print "server: quitting"
        conn.close()
        server_socket.close()
    conn.sendall(formed_response)
    conn.close()

    server_socket.close()


if __name__ == '__main__':
    # Create 10 sockets in main loops
    # import pdb; pdb.set_trace()
    socket_mains = [gevent.spawn(main, create_socket(port)) for port in range(10)]
    # Concurrently run the loops
    gevent.joinall(socket_mains)

    while True:
        try:
            time.sleep(.2)
        except KeyboardInterrupt:
            event.clear()
            sys.stdout.write('event: ' + str(event.isSet()))
            # Force .accept() to return.
            for port in range(10):
                socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM,
                    socket.IPPROTO_IP).connect(('127.0.0.1', 50000 + port))

            break
