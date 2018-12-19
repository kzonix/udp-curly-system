import logging
import socket
import asyncio
import uvloop

from server.router import RoutableServer
from server.server_logger import ServerLogging

"""
The asyncio module, introduced by PEP 3156, is a collection of network transports, protocols, 
and streams abstractions, with a pluggable event loop.
uvloop is a drop-in replacement of the built-in asyncio event loop.
uvloop makes asyncio fast. In fact, it is at least 2x faster than nodejs, gevent, 
as well as any other Python asynchronous framework. The performance of uvloop-based asyncio 
is close to that of Go programs.
"""
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.get_event_loop()

"""

"""
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)


class UdpSockServer(RoutableServer, ServerLogging):
    """

    """
    hostname = str
    port = int
    event_loop = loop
    server_sock = sock

    def __init__(self, hostname: str = "localhost", port: int = 3553):
        RoutableServer.__init__(self)
        self.hostname = hostname
        self.port = port
        self.__init_socket()

    def start(self):
        self.logger.info("Listening on %s:%d", self.hostname, self.port)
        try:
            loop.run_until_complete(self.__start())
        finally:
            loop.close()

    def stop(self):
        self.event_loop.close()

    def __init_socket(self):
        """

        :return:
        """
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.setblocking(False)
        self.server_sock.bind((self.hostname, self.port))
        self.logger.info("Initializing server instance - %r", self.server_sock)


    async def __start(self) -> None:
        """

        :return:
        """
        while True:
            data, addr = await self.__recvfrom(n_bytes=1024)
            self.logger.info("Message %r from %r ", data, addr)
            # TODO: add handler based on Protocol and data content
            await self.__sendto(data, addr)

    def __recvfrom(self, n_bytes, future=None, registered=False):
        fd = self.server_sock.fileno()
        if future is None:
            future = self.event_loop.create_future()
        if registered:
            self.event_loop.remove_reader(fd)

        try:
            data, addr = self.server_sock.recvfrom(n_bytes)
        except (IOError, BlockingIOError, InterruptedError):
            self.event_loop.add_reader(fd, self.__recvfrom, n_bytes, future, True)
        else:
            future.set_result((data, addr))
        return future

    def __sendto(self, data, addr, future=None, registered=False):
        fd = self.server_sock.fileno()
        if future is None:
            future = self.event_loop.create_future()
        if registered:
            self.event_loop.remove_writer(fd)

        try:
            n = self.server_sock.sendto(data, addr)
        except (IOError, BlockingIOError, InterruptedError):
            self.event_loop.add_writer(fd, self.__sendto, data, addr, future, True)
        else:
            future.set_result(n)
        return future
