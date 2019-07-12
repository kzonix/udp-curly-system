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
    """
    TODO: This will run the following commands:
     - init configuration sources (read configuration files: conf, yaml; read environment variables, read cli startup args)
     - init prestart hooks
     - server start
     - init shutdown hooks
    """
    server = UdpServer()

    try:
        default_logger.info("Starting...")
        server.start()
        # There should not be code after server start.
        # It can invoke 'loop.close' as a finally block of wrapped handler.
        # TODO: add mechanism of run/stop server hooks.
    except KeyboardInterrupt as err:
        server.stop()  # close underlying event loop in case of manual stop of the run process.
        default_logger.error("Server is stopping due to %r exception ", err)
    except (IOError, BlockingIOError, StopAsyncIteration) as err:
        server.stop()  # close underlying event loop in case of occasion blocking operation error.
        default_logger.exception("Unexpected exception: %r", err)
    except Exception as err:
        server.stop()  # close underlying event loop in case of occasion blocking operation error.
        default_logger.exception("Oops... %r", err)
    finally:
        sys.exit(0)  # stop system process
