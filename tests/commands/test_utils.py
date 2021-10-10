from aiohttp_lamp.commands.utils import *


def test_utils_create_header_cmd():
    assert create_header_cmd(0, 0) == b'\x00\x00\x00'
    assert create_header_cmd(0, 1) == b'\x00\x00\x01'
    assert create_header_cmd(10, 1) == b'\x0a\x00\x01'


def test_utils_parse_header_cmd():
    assert parse_header_cmd(b'\x00\x00\x00') == (0, 0)
    assert parse_header_cmd(b'\x00\x00\x01\xab') == (0, 1)
    assert parse_header_cmd(b'\x0a\x00\x01\xcd') == (10, 1)


def test_utils_create_cmd():
    assert create_cmd(0, 0, b'') == b'\x00\x00\x00'
    assert create_cmd(0, 0, b'\x00') == b'\x00\x00\x00\x00'
    assert create_cmd(0, 1, b'') == b'\x00\x00\x01'
    assert create_cmd(0, 1, b'\xab') == b'\x00\x00\x01\xab'
    assert create_cmd(10, 1, b'') == b'\x0a\x00\x01'
    assert create_cmd(10, 1, b'\xcd') == b'\x0a\x00\x01\xcd'


def test_utils_create_cmd_ON():
    assert create_cmd_ON() == b'\x12\x00\x00'
    assert create_cmd_ON(b'') == b'\x12\x00\x00'
    assert create_cmd_ON(b'\xab') == b'\x12\x00\x00\xab'


def test_utils_create_cmd_OFF():
    assert create_cmd_OFF() == b'\x13\x00\x00'
    assert create_cmd_OFF(b'') == b'\x13\x00\x00'
    assert create_cmd_OFF(b'\xab') == b'\x13\x00\x00\xab'


def test_utils_create_cmd_COLOR():
    assert create_cmd_COLOR(b'') == b'\x20\x00\x03'
    assert create_cmd_COLOR(b'\xab') == b'\x20\x00\x03\xab'
    assert create_cmd_COLOR(b'\xab\xcd') == b'\x20\x00\x03\xab\xcd'
    assert create_cmd_COLOR(b'\xab\xcd\xef') == b'\x20\x00\x03\xab\xcd\xef'
    assert create_cmd_COLOR(b'\xab\xcd\xef\x88') == b'\x20\x00\x03\xab\xcd\xef\x88'
