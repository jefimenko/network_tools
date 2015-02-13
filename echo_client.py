import socket
import sys


def create_client_socket():
    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)
    return client_socket


def comm(client_socket, message):
    client_socket.connect(('127.0.0.1', 50000))
    # Send argv from command line
    client_socket.sendall(', '.join(message))
    client_socket.shutdown(socket.SHUT_WR)


def receive(client_socket):
    reception = client_socket.recv(32)
    client_socket.close()
    return reception


if __name__ == '__main__':
    client_socket = create_client_socket()
    comm(client_socket, sys.argv[1:])
    print receive(client_socket)
