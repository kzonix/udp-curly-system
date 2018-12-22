from enum import IntEnum


class Protocol(IntEnum):
    pass


class BaseProtocol(IntEnum, Protocol):
    msg_pack = 1
    plain = 2
