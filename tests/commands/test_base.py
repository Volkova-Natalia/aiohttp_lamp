from aiohttp_lamp.commands.base import Base
from aiohttp_lamp.commands.consts import ValidateMsgRetval
from struct import Struct


# ------------------------------
def _get_tested_base():
    class TestedBase(Base):
        cmd_type = 0
        data_len = 0

        @property
        def struct(self) -> Struct:
            return self.header_struct

        def _execute(self, cmd: bytes):
            return None

    return TestedBase()
# ------------------------------


def test_base__parse_header_cmd():
    tested_base = _get_tested_base()
    tested_base._parse_header_cmd(b'\x12\x34\x56')
    assert tested_base._parsed_cmd_type == int.from_bytes(b'\x12', byteorder='big')
    assert tested_base._parsed_data_len == int.from_bytes(b'\x34\x56', byteorder='big')
    assert tested_base._parsed_data_len == 13398


def test_base__validate_msg():
    tested_base = _get_tested_base()
    assert tested_base._validate_msg(None) == ValidateMsgRetval.EMPTY_MSG
    assert tested_base._validate_msg('') == ValidateMsgRetval.EMPTY_MSG
    assert tested_base._validate_msg(b'') == ValidateMsgRetval.EMPTY_MSG
    assert tested_base._validate_msg(0) == ValidateMsgRetval.EMPTY_MSG
    assert tested_base._validate_msg(False) == ValidateMsgRetval.EMPTY_MSG

    assert tested_base._validate_msg('x12') == ValidateMsgRetval.INVALID_TYPE_MSG
    assert tested_base._validate_msg('\x12') == ValidateMsgRetval.INVALID_TYPE_MSG
    assert tested_base._validate_msg(0x12) == ValidateMsgRetval.INVALID_TYPE_MSG
    assert tested_base._validate_msg(True) == ValidateMsgRetval.INVALID_TYPE_MSG
    assert tested_base._validate_msg([0x12, 0x13]) == ValidateMsgRetval.INVALID_TYPE_MSG

    assert tested_base._validate_msg(b'\x12') == ValidateMsgRetval.INVALID_MSG_LENGTH
    assert tested_base._validate_msg(b'\x12\x34') == ValidateMsgRetval.INVALID_MSG_LENGTH
    assert tested_base._validate_msg(b'\x12\x34\x56') == ValidateMsgRetval.INVALID_MSG_LENGTH
    assert tested_base._validate_msg(b'\x12\x00\x01') == ValidateMsgRetval.INVALID_MSG_LENGTH
    assert tested_base._validate_msg(b'\x12\x01\x00\x34') == ValidateMsgRetval.INVALID_MSG_LENGTH

    assert tested_base._validate_msg(b'\x12\x00\x00') == ValidateMsgRetval.VALID_MSG
    assert tested_base._validate_msg(b'\x12\x00\x01\x34') == ValidateMsgRetval.VALID_MSG
    assert tested_base._validate_msg(b'\x12\x00\x02\x34\x56') == ValidateMsgRetval.VALID_MSG
