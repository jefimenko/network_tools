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


def receive_msg(server_socket, buffsize):
    conn, addr = server_socket.accept()
    message = ''
    keep_going = True
    while keep_going:
        pkt = conn.recv(buffsize)
        print repr(pkt)
        message = '{}{}'.format(message, pkt)

        # For a last packet of buffsize, this loop iterates one more time
        if len(pkt) < buffsize:
            keep_going = False
            print keep_going
    return conn, addr, message


def parse_request(header):
    header = header.split('\r\n')
    first_line = header[0].split()

    # Break up first_line
    try:
        method = first_line[0]
        uri = first_line[1]
        proto = first_line[2]
    except IndexError:
        pass

    if method != 'GET' or proto != 'HTTP/1.1':
        # Deny non-GET and non-HTTP/1.1 requests.
        raise ValueError(403, 'Forbidden')

    # Divide headers by line
    try:
        headers = []
        for line in header[1:]:
            headers.append(line)
    except IndexError:
        pass
    return uri, headers


def response_ok():
    response = """\
HTTP/1.1 200 OK\r\n\
"""
    return response


def response_error(e):
    response = """\
HTTP/1.1 {type} {cause}\r\n\
""".format(type=e[0], cause=e[1])
    return response


if __name__ == '__main__':
    buffsize = 8

    server_socket = create_server_socket()

    while True:
        conn, addr, message = receive_msg(server_socket, buffsize)
        # Cut up message
        message = message.split('\r\n\r\n')
        try:
            # All assignments up until a line that causes an exception persist.
            # Only bind symbols to parts of the request that are there.
            header = message[0]
            body = message[1]
            footer = message[2]
        except IndexError:
            pass

        try:
            # Parse request
            uri, headers = parse_request(header)
            print 'check'
            formed_response = response_ok()
            # Send the appropriate message
            # OK
        except Exception as e:
            # Errors
            print e[0]
            print e[1]
            formed_response = response_error(e)
        conn.sendall(formed_response)
        conn.close()
