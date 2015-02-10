import socket

server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
    socket.IPPROTO_IP)

server_socket.bind(('127.0.0.1', 50000))
server_socket.listen(1)
conn, addr = server_socket.accept()

print conn.recv(32)
conn.sendall('reply')
conn.close()