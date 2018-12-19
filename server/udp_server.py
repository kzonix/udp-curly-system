from server.environ import SERVER_CONFIG
from server.server_logger import RootServerLogger
from server.udp_sock import UdpSockServer


class UdpServer(UdpSockServer, RootServerLogger):
    """

    """

    def __init__(self, hostname: str = None,
                 port: int = None,
                 logger_config: dict = None
                 ):
        RootServerLogger.__init__(self)
        if hostname and port:
            super().__init__(hostname, port)
        elif SERVER_CONFIG.host and SERVER_CONFIG.port:
            super().__init__(hostname=SERVER_CONFIG.host, port=SERVER_CONFIG.port)
        else:
            super().__init__()
