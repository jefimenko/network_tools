import socket


def create_server_socket():
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)
    return server_socket


def comm(server_socket):
    server_socket.bind(('127.0.0.1', 50000))
    server_socket.listen(1)
    conn, addr = server_socket.accept()
    return conn, addr


def receive(conn):
    return conn.recv(32)


if __name__ == '__main__':
    buffsize = 8

    server_socket = create_server_socket()

    conn, addr = comm(server_socket)

    # try:
    # while True:
    message = ''
    keep_going = True
    while keep_going:
        pkt = receive(conn)
        message = '{}{}'.format(message, pkt)

        print message
        print len(message)
        # For a last packet of buffsize, it iterates one more time
        if len(pkt) < buffsize:
            keep_going = False
    conn.sendall(message)

    # Allow stopping server in console with KeyboardInterrupt
    # except KeyboardInterrupt:
    #     conn.close()
    #     server_socket.close()
