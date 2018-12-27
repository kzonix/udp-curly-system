import socket

UDP_ADDR = 'localhost'
UDP_PORT = 5006

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((UDP_ADDR, UDP_PORT))
print("Server started. %s:%d" % (UDP_ADDR, UDP_PORT))

while True:
    data, addr = sock.recvfrom(2048)  # buffer size is 1024 bytes
    print("Received message %s from %s" % (data.decode(), addr))
    sock.sendto(data.decode()[::-1].encode(), addr)
