import ast
import os
import sys
import dotenv
import logging

from server.logger import default_logger

HOST = "UDP_HOST"
PORT = "UDP_PORT"
LOG_LEVEL = "LOG_LEVEL"


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def override_with_cli_args():
    cli_args = sys.argv
    for arg in cli_args:
        if "=" not in arg:
            continue
        key, value = arg.split('=', 1)
        key = key.strip().upper()
        value = ast.literal_eval(value.strip())
        os.environ.setdefault(key, str(value))


class ServerConfig(metaclass=Singleton):
    host: str = None
    port: int = None

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        dotenv.load()
        override_with_cli_args()
        try:
            host = os.environ[HOST]
            port = os.environ[PORT]
            log_level = os.environ[LOG_LEVEL]
            logging.basicConfig(level=log_level)
            self.host = host
            self.port = port
        except KeyError as err:
            default_logger.error("Can`t configure server from environ-configuration. %r", err)
