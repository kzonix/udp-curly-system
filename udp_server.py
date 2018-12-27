import logging
import multiprocessing
import socket


class UdpServer(object):
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
        self.logger.debug("Listening on %s:%d", self.hostname, self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        while True:
            conn, address = self.socket.accept()
            self.logger.debug("Got connection")
            process = multiprocessing.Process(target=handle, args=(conn, address))
            process.daemon = True
            process.start()
            self.logger.debug("Started process %r", process)

    def __get_default_logger(self):
        logging.basicConfig(level=logging.DEBUG)
        return logging.getLogger("UDP-SERVER :::%d" % self.port)


def handle(connection, address):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("process-%r" % (address,))
    try:
        logger.debug("Connected %r at %r", connection, address)
        while True:
            data = connection.recv(1024)
            if data == "":
                logger.debug("Socket closed remotely")
                break
            logger.debug("Received data %r", data)
            connection.sendall(data)
            logger.debug("Sent data")
    except IOError as error:
        logger.exception("Problem handling request", error)
    finally:
        logger.debug("Closing socket")
        connection.close()
