import multiprocessing

from udp_server import UdpServer

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    server = UdpServer("0.0.0.0", 9000)
    try:
        logging.info("Listening")
        server.start()
    except IOError as err:
        logging.exception("Unexpected exception", err)
    finally:
        logging.info("Shutting down")
        for process in multiprocessing.active_children():
            logging.info("Shutting down process %r", process)
            process.terminate()
            process.join()
            logging.info("All done")
