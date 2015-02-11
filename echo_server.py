import socket
import email.utils


def create_server_socket():
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)
    # Set up the socket
    server_socket.bind(('127.0.0.1', 50000))
    server_socket.listen(1)
    return server_socket


def response_ok():
    return """
        HTTP/1.1 200 OK\r\n
        Content-Type: text/plain\r\n
        \r\n
        Hey you.\r\n
    """


def response_error():
    pass


def parse_request(request_string):
    pass


if __name__ == '__main__':
    buffsize = 8

    server_socket = create_server_socket()

    while True:
        conn, addr = server_socket.accept()

        message = ''
        keep_going = True
        while keep_going:
            pkt = conn.recv(buffsize)
            print repr(pkt)
            message = '{}{}'.format(message, pkt)

            # For a last packet of buffsize, this loop iterates one more time
            if (len(pkt) < buffsize) or (len(pkt) == 0):
                keep_going = False
                print keep_going
        conn.sendall(message)
        conn.close()
