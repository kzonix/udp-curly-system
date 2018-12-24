from udp_server import UdpServer

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    server = UdpServer()
    try:
        logging.info("Listening...")
        server.start()
    except:
        logging.exception("Unexpected exception")
    finally:
        server.stop()
