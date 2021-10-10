from enum import Enum
from struct import Struct


class CmdFormat(Enum):
    TYPE_POS = 0
    TYPE_SIZE = 1
    DATA_LENGTH_POS = TYPE_POS + TYPE_SIZE
    DATA_LENGTH_SIZE = 2
    HANDLER_SIZE = TYPE_SIZE + DATA_LENGTH_SIZE
    DATA_POS = DATA_LENGTH_POS + DATA_LENGTH_SIZE

    HEADER_FORMAT = '>BH'
    HEADER_STRUCT = Struct(HEADER_FORMAT)


class CmdON(Enum):
    TYPE = int.from_bytes(b'\x12', byteorder='big')
    DATA_LENGTH = 0
    STRUCT = Struct(CmdFormat.HEADER_FORMAT.value + str(DATA_LENGTH) + 's')


class CmdOFF(Enum):
    TYPE = int.from_bytes(b'\x13', byteorder='big')
    DATA_LENGTH = 0
    STRUCT = Struct(CmdFormat.HEADER_FORMAT.value + str(DATA_LENGTH) + 's')


class CmdCOLOR(Enum):
    TYPE = int.from_bytes(b'\x20', byteorder='big')
    DATA_LENGTH = 3
    STRUCT = Struct(CmdFormat.HEADER_FORMAT.value + str(DATA_LENGTH) + 's')


class ValidateMsgRetval(Enum):
    EMPTY_MSG = -1
    INVALID_TYPE_MSG = -2
    INVALID_MSG_LENGTH = -3
    VALID_MSG = 1


class ValidateCmdRetval(Enum):
    UNKNOWN_CMD = -1
    INVALID_CMD_LENGTH = -2
    VALID_CMD = 1


class CmdRunRetval(Enum):
    INVALID_MSG = -1
    INVALID_CMD = -2
    CMD_COMPLETED_SUCCESSFULLY = 1
