from logging import Logger, getLogger


class ServerLogging:
    logger: Logger = None


class RootServerLogger(ServerLogging):
    logger = None

    def __init__(self, name: str = " <UPD - Server> ",
                 log_config: dict = None):
        self.logger = getLogger(name)
