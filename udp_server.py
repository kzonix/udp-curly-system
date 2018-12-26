import logging
import multiprocessing
import socket
import asyncio


class UdpServer(object):
    """

    """
    event_loop = asyncio.get_running_loop()
    logger = None
    socket = None
    hostname = str
    port = int

    def __init__(self):
        self.__init__("localhost", 30981)

    def __init__(self, hostname: str, port: int):
        self.hostname = hostname
        self.port = port
        self.logger = self.__get_default_logger()

    def start(self):
        try:
            self.event_loop.run_until_complete(self.__start())
        finally:
            self.event_loop.close()

    def __init_socket(self):
        """

        :return:
        """
        self.logger.debug("Listening on %s:%d", self.hostname, self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(False)
        self.socket.bind((self.hostname, self.port))

    async def __start(self):
        self.__init_socket()
        while True:
            data, addr = await self.__receive_from(1024)
            #
            n_bytes = await self.__send_to(data, addr)

    # TODO: add logging of input messages and basic routing implementation
    def __receive_from(self, n_bytes, future=None, registered=False):
        fd = self.socket.fileno()
        if future is None:
            future = self.event_loop.create_future()
        if registered:
            self.event_loop.remove_reader(fd)

        try:
            data, addr = self.socket.recvfrom(n_bytes)
        except (BlockingIOError, InterruptedError):
            self.event_loop.add_reader(fd, self.__receive_from, self.event_loop, self.socket, n_bytes, future, True)
        else:
            future.set_result((data, addr))
        return future

    # TODO: provide configurable mechanism of response manipulation
    def __send_to(self, data, addr, future=None, registered=False):
        fd = self.socket.fileno()
        if future is None:
            future = self.event_loop.create_future()
        if registered:
            self.event_loop.remove_writer(fd)
        if not data:
            return

        try:
            # TODO: add handler for 'data' arg
            n = self.socket.sendto(data, addr)
        except (BlockingIOError, InterruptedError):
            self.event_loop.add_writer(fd, self.__send_to, self.event_loop, self.socket, data, addr, future, True)
        else:
            future.set_result(n)
        return future

    def __get_default_logger(self):
        """

        :return:
        """
        logging.basicConfig(level=logging.DEBUG)
        return logging.getLogger("UDP-SERVER :::%d" % self.port)
