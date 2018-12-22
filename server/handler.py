from typing import AnyStr


class Handler:
    _name: str = ""
    _handler = None

    def __init__(self, name: str, fn):
        self._name = name
        self._handler = fn

    def get_handler(self):
        return self._handler

    def get_handler_name(self):
        return self._handler
