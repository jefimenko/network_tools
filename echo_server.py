import socket


def create_server_socket():
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)
    # Set up the server socket
    server_socket.bind(('127.0.0.1', 50000))
    server_socket.listen(1)
    return server_socket


def response_ok():
    return """\
HTTP/1.1 200 OK\r\n\
Content-Type: text/plain\r\n\r\n\
Hey you.\r\n\
"""


def response_error(e):
    return """\
HTTP/1.1 {error}\r\n\
\r\n\
{cause}\r\n\
    """.format(error=e.args[0], cause=e.args[1])


def parse_request(request_string):
    first_line = request_string.split('\r\n')[0]
    first_line = first_line.split()

    if request_protocol_validator(first_line):
        return first_line[1]


def request_protocol_validator(first_line):
    try:
        method, protocol = first_line[0], first_line[2]
    except IndexError:
        # By returning False, have the server continue to close the current 
        # connection and wait for the next request without responding.
        return False

    if method != 'GET':
        raise ValueError('403', 'GET method only.')
    if protocol != 'HTTP/1.1':
        raise ValueError('403', 'HTTP/1.1 only.')

    if method == 'GET' and protocol == 'HTTP/1.1':
        return True


if __name__ == '__main__':
    buffsize = 8

    server_socket = create_server_socket()

    while True:
        # Open a connection to a client upon request.
        conn, addr = server_socket.accept()

        message = ''
        keep_going = True
        # Receive a message from a client.
        while keep_going:
            pkt = conn.recv(buffsize)
            # print repr(pkt)
            message = '{}{}'.format(message, pkt)

            # For a last packet of buffsize, this loop iterates one more time.
            # If the message is over, stop receiving.
            if (len(pkt) < buffsize) or (len(pkt) == 0):
                keep_going = False
                print keep_going
                print repr(message)

        # Parse the message and send the appropriate response.
        try:
            # For now, don't do anything with returned URI from message.
            if parse_request(message):
                conn.sendall(response_ok())
        except ValueError as e:
            conn.sendall(response_error(e))

        # Close the connection after sending a response.
        conn.close()
