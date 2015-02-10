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
    return conn, addr = server_socket.accept()


def receive(conn):
    print conn.recv(32)
    conn.sendall('reply')
    conn.close()
