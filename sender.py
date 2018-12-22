import socket

UDP_IP = "localhost"
UDP_PORT = 3553
MESSAGE = b"Hello, World!"

sock = socket.socket(socket.AF_INET,  # Internet

                     socket.SOCK_DGRAM)  # UDP
while True:
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    print('waiting to receive')
    data, server = sock.recvfrom(4096)
    print('received "%s"' % data)
