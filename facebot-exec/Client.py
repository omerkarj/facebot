import socket
import sys
import cv2
import numpy as np
import base64
from PIL import Image
from StringIO import StringIO

def readb64(base64_string):
    sbuf = StringIO()
    sbuf.write(base64.b64decode(base64_string))
    pimg = Image.open(sbuf)
    return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Connect the socket to the port where the server is listening
def start():
    server_address = ('localhost', 1337)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)

def stop():
    print >> sys.stderr, 'closing socket'
    sock.close()
    cv2.waitKey(0)

def sendLineToServer(line):
    try:
        # Send data
        message = str(line) + '<EOL>'
        # print >> sys.stderr, 'sending "%s"' % message
        sock.sendall(message)

    except Exception, e:
        print >> sys.stderr, e

def getNextFrameFromServer():
    try:
        # Send data
        message = '<NEXT>'
        # print >> sys.stderr, 'sending "%s"' % message
        sock.sendall(message)

        # Look for the response
        img_str = ''

        while not img_str.endswith('<EOF>'):
            data_str = sock.recv(16384)
            img_str += data_str

            # print >> sys.stderr, 'received "%s"' % data_str

        # when frame received
        clean_img_str = img_str.replace('<EOF>', '')
        if clean_img_str == '<NO_CHANGE>':
            return ''
        else:
            return readb64(clean_img_str)


    except Exception, e:
        print >> sys.stderr, e

def sendNextPhaseToServer():
    try:
        # Send data
        message = '<PHASE>'
        print >> sys.stderr, 'sending "%s"' % message
        sock.sendall(message)

    except Exception, e:
        print >> sys.stderr, e

def sendResetToServer():
    try:
        # Send data
        message = '<RESET>'
        print >> sys.stderr, 'sending "%s"' % message
        sock.sendall(message)

    except Exception, e:
        print >> sys.stderr, e

def sendQuitToServer():
    try:
        # Send data
        message = '<QUIT>'
        print >> sys.stderr, 'sending "%s"' % message
        sock.sendall(message)

    except Exception, e:
        print >> sys.stderr, e
