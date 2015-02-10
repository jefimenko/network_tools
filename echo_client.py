import socket
import sys

client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
    socket.IPPROTO_IP)

client_socket.connect(('127.0.0.1', 50000))
# Send argv from command line
client_socket.sendall(', '.join(sys.argv[1:]))
client_socket.shutdown(socket.SHUT_WR)

print client_socket.recv(32)
client_socket.close()