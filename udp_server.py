import logging
import socket
import asyncio

"""

"""
loop = asyncio.get_event_loop()
"""

"""
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)


class UdpServer(object):
    """

    """
    logger = None
    hostname = str
    port = int
    event_loop = loop
    server_sock = sock

    def __init__(self, hostname: str = "localhost", port: int = 3553):
        self.hostname = hostname
        self.port = port
        self.logger = self.__get_default_logger()
        self.__init_socket()

    def start(self):
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
        self.logger.debug("Listening on %s:%d", self.hostname, self.port)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.setblocking(False)
        self.server_sock.bind((self.hostname, self.port))

    async def __start(self):
        """

        :return:
        """
        while True:
            data, addr = await self.__recvfrom(n_bytes=1024)
            self.logger.info("Message %r from %r ", data, addr)
            await self.__sendto(data, addr)

    def __recvfrom(self, n_bytes, future=None, registered=False):
        fd = self.server_sock.fileno()
        if future is None:
            future = self.event_loop.create_future()
        if registered:
            self.event_loop.remove_reader(fd)

        try:
            data, addr = self.server_sock.recvfrom(n_bytes)
        except (BlockingIOError, InterruptedError):
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
        if not data:
            return

        try:
            n = self.server_sock.sendto(data, addr)
        except (BlockingIOError, InterruptedError):
            self.event_loop.add_writer(fd, self.__sendto, data, addr, future, True)
        else:
            future.set_result(n)
        return future

    def __get_default_logger(self):
        """

        :return:
        """
        logging.basicConfig(level=logging.DEBUG)
        return logging.getLogger("UDP-SERVER :::%d" % self.port)
