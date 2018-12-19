from server.logger import default_logger
from server.udp_server import UdpServer
import sys


def exception_handler(exctype, value, traceback):
    if exctype == KeyboardInterrupt:
        default_logger.exception("Unexpected exception: %r", value)
    else:
        sys.__excepthook__(exctype, value, traceback)


sys.excepthook = exception_handler

if __name__ == "__main__":

    server = UdpServer()

    try:
        default_logger.info("Starting...")
        server.start()
    except KeyboardInterrupt as err:
        default_logger.error("Server is stopping due to %r exception ", err)
        server.stop()
    except (IOError, BlockingIOError, StopAsyncIteration) as err:
        default_logger.exception("Unexpected exception: %r", err)
    except Exception as err:
        default_logger.exception("Oops... %r", err)
    finally:
        server.stop()
        sys.exit(0)
