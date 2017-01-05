import socket
import sys
import cv2
import numpy as np
import base64
from PIL import Image
from StringIO import StringIO

def readb64(base64_string):
    print >> sys.stderr, '1'
    sbuf = StringIO()
    print >> sys.stderr, '2'
    sbuf.write(base64.b64decode(base64_string))
    print >> sys.stderr, '3'
    pimg = Image.open(sbuf)
    print >> sys.stderr, '4'
    return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 1337)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    num = 0
    # Send data
    while True:
        message = '(' + `(num % 5)` + ',' + `(num % 20)` + ')<EOF>'
        print >> sys.stderr, 'sending "%s"' % message
        sock.sendall(message)

        # Look for the response
        amount_received = 0
        img_str = ''
        frame_buf = []

        while not img_str.endswith('=='):
            data_str = sock.recv(16384)
            img_str += data_str
            print >> sys.stderr, 'received "%s"' % data_str

        if len(img_str) > 0:
            frame = readb64(img_str)
            print >> sys.stderr, frame
            # if frame:
            cv2.imshow('game', frame)
            print >> sys.stderr, num
        num += 1
        print >> sys.stderr, num

except Exception, e:
    print >> sys.stderr, e
finally:
    print >> sys.stderr, 'closing socket'
    sock.close()
    cv2.waitKey(0)