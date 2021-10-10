from aiohttp_lamp.commands.off import Off
from aiohttp_lamp.commands.consts import CmdOFF, ValidateCmdRetval, CmdRunRetval
from aiohttp_lamp.commands.utils import create_cmd, create_cmd_OFF


# ------------------------------
OFF_TYPE = CmdOFF.TYPE.value
OFF_DATA_LENGTH = CmdOFF.DATA_LENGTH.value
# ------------------------------


def test_off__validate_cmd():
    tested_off = Off()
    cmd = b'\x00\x00\x00'
    tested_off._parse_header_cmd(cmd)
    assert tested_off._validate_cmd(cmd) == ValidateCmdRetval.UNKNOWN_CMD
    cmd = create_cmd(OFF_TYPE - 1, OFF_DATA_LENGTH, b'')
    tested_off._parse_header_cmd(cmd)
    assert tested_off._validate_cmd(cmd) == ValidateCmdRetval.UNKNOWN_CMD
    cmd = create_cmd(OFF_TYPE + 1, OFF_DATA_LENGTH, b'')
    tested_off._parse_header_cmd(cmd)
    assert tested_off._validate_cmd(cmd) == ValidateCmdRetval.UNKNOWN_CMD

    cmd = create_cmd(OFF_TYPE, OFF_DATA_LENGTH + 1, b'\x34')
    tested_off._parse_header_cmd(cmd)
    assert tested_off._validate_cmd(cmd) == ValidateCmdRetval.INVALID_CMD_LENGTH

    cmd = create_cmd_OFF()
    tested_off._parse_header_cmd(cmd)
    assert tested_off._validate_cmd(cmd) == ValidateCmdRetval.VALID_CMD


def test_off_run():
    tested_off = Off()
    assert tested_off.run(None) == CmdRunRetval.INVALID_MSG
    assert tested_off.run(b'') == CmdRunRetval.INVALID_MSG
    assert tested_off.run(0x13) == CmdRunRetval.INVALID_MSG
    assert tested_off.run(OFF_TYPE) == CmdRunRetval.INVALID_MSG
    assert tested_off.run(create_cmd_OFF(b'\x34\x56\x78\x9a\xbc\xde')) == CmdRunRetval.INVALID_MSG

    assert tested_off.run(create_cmd(OFF_TYPE - 1, OFF_DATA_LENGTH, b'')) == CmdRunRetval.INVALID_CMD
    assert tested_off.run(create_cmd(OFF_TYPE, OFF_DATA_LENGTH + 1, b'\x34')) == CmdRunRetval.INVALID_CMD

    assert tested_off.run(create_cmd_OFF()) == CmdRunRetval.CMD_COMPLETED_SUCCESSFULLY
