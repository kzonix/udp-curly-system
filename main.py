from udp_server import UdpServer
import sys
import logging

logging.basicConfig(level=logging.DEBUG)


def exception_handler(exctype, value, traceback):
    if exctype == KeyboardInterrupt:
        logging.exception("Unexpected exception: %r", value)
    else:
        sys.__excepthook__(exctype, value, traceback)


sys.excepthook = exception_handler

if __name__ == "__main__":

    server = UdpServer()
    try:
        logging.info("Listening...")
        server.start()
    except (KeyboardInterrupt, IOError, BlockingIOError, StopAsyncIteration) as err:
        logging.exception("Unexpected exception: %r", err)
    finally:
        server.stop()
