from .consts import CmdFormat, CmdON, CmdOFF, CmdCOLOR


HEADER_STRUCT = CmdFormat.HEADER_STRUCT.value

ON_TYPE = CmdON.TYPE.value
ON_DATA_LENGTH = CmdON.DATA_LENGTH.value

OFF_TYPE = CmdOFF.TYPE.value
OFF_DATA_LENGTH = CmdOFF.DATA_LENGTH.value

COLOR_TYPE = CmdCOLOR.TYPE.value
COLOR_DATA_LENGTH = CmdCOLOR.DATA_LENGTH.value


def create_header_cmd(cmd_type: int, data_len: int) -> bytes:
    return HEADER_STRUCT.pack(cmd_type, data_len)


def parse_header_cmd(cmd: bytes) -> tuple:
    return HEADER_STRUCT.unpack_from(cmd)


def create_cmd(cmd_type: int, data_len: int, data: bytes) -> bytes:
    return create_header_cmd(cmd_type, data_len) + data


def create_cmd_ON(data: bytes = b'') -> bytes:
    return create_cmd(ON_TYPE, ON_DATA_LENGTH, data)


def create_cmd_OFF(data: bytes = b'') -> bytes:
    return create_cmd(OFF_TYPE, OFF_DATA_LENGTH, data)


def create_cmd_COLOR(color: bytes) -> bytes:
    return create_cmd(COLOR_TYPE, COLOR_DATA_LENGTH, color)
