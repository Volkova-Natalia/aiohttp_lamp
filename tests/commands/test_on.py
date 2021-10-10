from aiohttp_lamp.commands.on import On
from aiohttp_lamp.commands.consts import CmdON, ValidateCmdRetval, CmdRunRetval
from aiohttp_lamp.commands.utils import create_cmd, create_cmd_ON


# ------------------------------
ON_TYPE = CmdON.TYPE.value
ON_DATA_LENGTH = CmdON.DATA_LENGTH.value
# ------------------------------


def test_on__validate_cmd():
    tested_on = On()
    cmd = b'\x00\x00\x00'
    tested_on._parse_header_cmd(cmd)
    assert tested_on._validate_cmd(cmd) == ValidateCmdRetval.UNKNOWN_CMD
    cmd = create_cmd(ON_TYPE - 1, ON_DATA_LENGTH, b'')
    tested_on._parse_header_cmd(cmd)
    assert tested_on._validate_cmd(cmd) == ValidateCmdRetval.UNKNOWN_CMD
    cmd = create_cmd(ON_TYPE + 1, ON_DATA_LENGTH, b'')
    tested_on._parse_header_cmd(cmd)
    assert tested_on._validate_cmd(cmd) == ValidateCmdRetval.UNKNOWN_CMD

    cmd = create_cmd(ON_TYPE, ON_DATA_LENGTH + 1, b'\x34')
    tested_on._parse_header_cmd(cmd)
    assert tested_on._validate_cmd(cmd) == ValidateCmdRetval.INVALID_CMD_LENGTH

    cmd = create_cmd_ON()
    tested_on._parse_header_cmd(cmd)
    assert tested_on._validate_cmd(cmd) == ValidateCmdRetval.VALID_CMD


def test_on_run():
    tested_on = On()
    assert tested_on.run(None) == CmdRunRetval.INVALID_MSG
    assert tested_on.run(b'') == CmdRunRetval.INVALID_MSG
    assert tested_on.run(0x12) == CmdRunRetval.INVALID_MSG
    assert tested_on.run(ON_TYPE) == CmdRunRetval.INVALID_MSG
    assert tested_on.run(create_cmd_ON(b'\x34\x56\x78\x9a\xbc\xde')) == CmdRunRetval.INVALID_MSG

    assert tested_on.run(create_cmd(ON_TYPE - 1, ON_DATA_LENGTH, b'')) == CmdRunRetval.INVALID_CMD
    assert tested_on.run(create_cmd(ON_TYPE, ON_DATA_LENGTH + 1, b'\x34')) == CmdRunRetval.INVALID_CMD

    assert tested_on.run(create_cmd_ON()) == CmdRunRetval.CMD_COMPLETED_SUCCESSFULLY
