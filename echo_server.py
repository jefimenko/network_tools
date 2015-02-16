import socket
import threading
import os
import time
from urlparse import urlparse
from datetime import datetime

# Full path to /webrootfolder.
RESOURCES_DIR = os.path.abspath('webroot')


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
    """
    Receive a string from a client.

    Wait until a client connects, then keep receiving the message in chunks
    equal to buffsize until the message is over, and return the connection,
    address and message.
    """
    conn, addr = server_socket.accept()

    message = ''
    keep_going = True
    while keep_going:
        pkt = conn.recv(buffsize)
        print 'server: ' + repr(pkt)
        message = '{}{}'.format(message, pkt)

        # For a last packet of buffsize, this loop iterates one more time
        if len(pkt) < buffsize:
            keep_going = False
            print keep_going

    return conn, addr, message


def parse_request(header):
    """
    Return the uri.
    """
    header = header.split('\r\n')
    first_line = header[0]

    first_line = first_line.split(' ')

    # Break up first_line
    try:
        method = first_line[0]
        uri = first_line[1]
        proto = first_line[2]
    except IndexError:
        pass

    if len(first_line) < 3:
        # For requests that are invalid due missing information:
        raise ValueError(400, 'Bad Request')
    # When .accept() is interupted to kill the server, method will not have
    # been bound at the point the script continues after .accept() is forced
    # to return, UnboundLocalError needs to be handled where parse_request()
    # is being called.
    elif method != 'GET' or proto != 'HTTP/1.1':
        # Deny non-GET and non-HTTP/1.1 requests.
        raise ValueError(403, 'Forbidden')

    return uri


def response_ok(content_type=None, body=None):
    response = """\
HTTP/1.1 200 OK\r\n\
Date: {date}\r\n\
Content-type: {content_type}\r\n\
\r\n\
{body}\r\n\
""".format(date=datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'),
           content_type=content_type,
           body=body)
    return response


def response_error(e):
    response = """\
HTTP/1.1 {type} {cause}\r\n\
""".format(type=e[0], cause=e[1])
    return response


def resolve_uri(uri):
    # Form uri into one useable for finding things
    parsed = urlparse(uri)
    file_name = os.path.split(parsed.path)[1]
    file_location = os.path.join(RESOURCES_DIR, file_name)
    # Find thing
    target, ext = os.path.splitext(file_location)

    # if a directory, return html rep of the directory

    body = target
    content_type = None
    if ext == '.html':
        content_type = 'text/html'
        with open(file_location) as f:
            body = f.read()
    elif ext == '.txt':
        content_type = 'text/plain'
        with open(file_location) as f:
            body = f.read()
    elif not ext:
        content_type = 'text/html'

    return content_type, body


def main(event):
    buffsize = 64

    server_socket = create_server_socket()

    while event.isSet():
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
            break
        conn.sendall(formed_response)
        conn.close()

    server_socket.close()


if __name__ == '__main__':
    event = threading.Event()
    event.set()

    t = threading.Thread(target=main, args=(event,))
    t.start()

    while True:
        try:
            time.sleep(.5)
        except KeyboardInterrupt:
            event.clear()
            print 'event: ' + str(event.isSet())
            # Force .accept() to return.
            socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM,
                socket.IPPROTO_IP).connect(('127.0.0.1', 50000))

            print 'checkout\n'
            break
