import socket
import threading
import os, sys
import time
import urllib
from urlparse import urlparse
from datetime import datetime

# Full path to /webrootfolder.
RESOURCES_DIR = os.path.dirname(os.path.abspath('webroot'))


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
        sys.stdout.write('server: ' + repr(pkt))
        message = '{}{}'.format(message, pkt)

        # For a last packet of buffsize, this loop iterates one more time
        if len(pkt) < buffsize:
            keep_going = False
            sys.stdout.write(str(keep_going))

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
Content-length: {content_length}\r\n\
\r\n\
{body}\r\n\
""".format(date=datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'),
           content_type=content_type,
           content_length=len(str(body)),
           body=body)
    return response


def response_error(e):
    response = """\
HTTP/1.1 {type} {cause}\r\n\
Date: {date}\r\n\
\r\n\
{type} {cause}\r\n\
""".format(type=e[0],
           cause=e[1],
           date=datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'))
    return response


def resolve_uri(uri):
    # Form uri into one useable for finding things
    parsed = urlparse(uri)
    req_directory, file_name = os.path.split(parsed.path)
    # Absolute file path
    req_directory = os.path.abspath(req_directory[1:])

    file_location = os.path.join(req_directory, file_name)
    target, ext = os.path.splitext(file_location)

    if not os.path.exists(file_location):
        raise ValueError(404, 'File Not Found')

    content_type = None
    if ext == '.html':
        content_type = 'text/html'
        with open(file_location) as f:
            body = f.read()
    elif ext == '.txt' or ext == '.py':
        content_type = 'text/plain'
        with open(file_location) as f:
            body = f.read()
    elif ext == '.jpg' or ext == '.png':
        content_type = 'image/gif'
        body = urllib.urlopen(urllib.pathname2url(file_location)).read()
    elif not ext:
        content_type = 'text/html'
        body = '<p>{}</p>'.format(os.path.split(target)[1])
        for item in os.listdir(target):
            body = '{}<p><a href="{}">{}</a></p>'.format(
                body, item, item)
    else:
        raise ValueError(404, 'File Not Found')

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
            time.sleep(.2)
        except KeyboardInterrupt:
            event.clear()
            sys.stdout.write('event: ' + str(event.isSet()))
            # Force .accept() to return.
            print 'checking out'
            socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM,
                socket.IPPROTO_IP).connect(('127.0.0.1', 50000))

            break
