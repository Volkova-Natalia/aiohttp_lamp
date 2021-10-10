from aiohttp_lamp.commands.color import Color
from aiohttp_lamp.commands.consts import CmdCOLOR, ValidateCmdRetval, CmdRunRetval
from aiohttp_lamp.commands.utils import create_cmd, create_cmd_COLOR


# ------------------------------
COLOR_TYPE = CmdCOLOR.TYPE.value
COLOR_DATA_LENGTH = CmdCOLOR.DATA_LENGTH.value
# ------------------------------


def test_color__get_color_from_cmd():
    tested_color = Color()
    assert tested_color._get_color_from_cmd(b'\x20\x00\x03\x34\x56\x78') == b'\x34\x56\x78'


def test_color__validate_cmd():
    tested_color = Color()
    cmd = b'\x00\x00\x00'
    tested_color._parse_header_cmd(cmd)
    assert tested_color._validate_cmd(cmd) == ValidateCmdRetval.UNKNOWN_CMD
    cmd = create_cmd(COLOR_TYPE - 1, COLOR_DATA_LENGTH, b'\x34\x56\x78')
    tested_color._parse_header_cmd(cmd)
    assert tested_color._validate_cmd(cmd) == ValidateCmdRetval.UNKNOWN_CMD
    cmd = create_cmd(COLOR_TYPE + 1, COLOR_DATA_LENGTH, b'\x34\x56\x78')
    tested_color._parse_header_cmd(cmd)
    assert tested_color._validate_cmd(cmd) == ValidateCmdRetval.UNKNOWN_CMD

    cmd = create_cmd(COLOR_TYPE, COLOR_DATA_LENGTH + 1, b'\x34\x56\x78\x9a')
    tested_color._parse_header_cmd(cmd)
    assert tested_color._validate_cmd(cmd) == ValidateCmdRetval.INVALID_CMD_LENGTH

    cmd = create_cmd_COLOR(b'\x34\x56\x78')
    tested_color._parse_header_cmd(cmd)
    assert tested_color._validate_cmd(cmd) == ValidateCmdRetval.VALID_CMD


def test_color_run():
    tested_color = Color()
    assert tested_color.run(None) == CmdRunRetval.INVALID_MSG
    assert tested_color.run(b'') == CmdRunRetval.INVALID_MSG
    assert tested_color.run(0x20) == CmdRunRetval.INVALID_MSG
    assert tested_color.run(COLOR_TYPE) == CmdRunRetval.INVALID_MSG
    assert tested_color.run(create_cmd_COLOR(b'')) == CmdRunRetval.INVALID_MSG
    assert tested_color.run(create_cmd_COLOR(b'\x34\x56\x78\x9a')) == CmdRunRetval.INVALID_MSG

    assert tested_color.run(create_cmd(COLOR_TYPE - 1, COLOR_DATA_LENGTH, b'\x34\x56\x78')) == CmdRunRetval.INVALID_CMD
    assert tested_color.run(create_cmd(COLOR_TYPE, COLOR_DATA_LENGTH + 1, b'\x34\x56\x78\x9a')) == CmdRunRetval.INVALID_CMD

    assert tested_color.run(create_cmd_COLOR(b'\x34\x56\x78')) == CmdRunRetval.CMD_COMPLETED_SUCCESSFULLY
