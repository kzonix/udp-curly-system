import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5006
MESSAGE = b"Hello, World!"

sock = socket.socket(socket.AF_INET,  # Internet

                     socket.SOCK_DGRAM)  # UDP

sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
print('waiting to receive')
data, server = sock.recvfrom(4096)
print('received "%s"' % data)

