from aiohttp_lamp.lamp import Lamp, StateLamp
from aiohttp_lamp.commands.on import On
from aiohttp_lamp.commands.off import Off
from aiohttp_lamp.commands.color import Color


def test_lamp_init():
    tested_lamp = Lamp()
    assert tested_lamp.state == StateLamp.OFF
    assert tested_lamp.color == b'\x00\x00\x00'
    assert isinstance(tested_lamp._cmd_handlers, list)
    assert len(tested_lamp._cmd_handlers) == 3
    assert isinstance(tested_lamp._cmd_handlers[0], On)
    assert isinstance(tested_lamp._cmd_handlers[1], Off)
    assert isinstance(tested_lamp._cmd_handlers[2], Color)


def test_lamp_turn_on():
    tested_lamp = Lamp()
    tested_lamp.turn_on()
    assert tested_lamp.state == StateLamp.ON

    tested_lamp.turn_off()
    tested_lamp.turn_on()
    assert tested_lamp.state == StateLamp.ON


def test_lamp_turn_off():
    tested_lamp = Lamp()
    tested_lamp.turn_off()
    assert tested_lamp.state == StateLamp.OFF

    tested_lamp.turn_on()
    tested_lamp.turn_off()
    assert tested_lamp.state == StateLamp.OFF


def test_lamp_change_color():
    tested_lamp = Lamp()
    tested_lamp.change_color(b'\x12\x34\x56')
    assert tested_lamp.color == b'\x12\x34\x56'

    tested_lamp.change_color(b'\x78\x9a\xbc')
    assert tested_lamp.color == b'\x78\x9a\xbc'


def test_lamp_execute_cmd_success():
    tested_lamp = Lamp()
    tested_lamp.execute_cmd(b'\x12\x00\x00')
    assert tested_lamp.state == StateLamp.ON
    assert tested_lamp.color == b'\x00\x00\x00'

    tested_lamp.execute_cmd(b'\x12\x00\x00')
    assert tested_lamp.state == StateLamp.ON
    assert tested_lamp.color == b'\x00\x00\x00'

    tested_lamp.execute_cmd(b'\x13\x00\x00')
    assert tested_lamp.state == StateLamp.OFF
    assert tested_lamp.color == b'\x00\x00\x00'

    tested_lamp.execute_cmd(b'\x12\x00\x00')
    assert tested_lamp.state == StateLamp.ON
    assert tested_lamp.color == b'\x00\x00\x00'

    tested_lamp.execute_cmd(b'\x20\x00\x03\x34\x56\x78')
    assert tested_lamp.state == StateLamp.ON
    assert tested_lamp.color == b'\x34\x56\x78'

    tested_lamp.execute_cmd(b'\x13\x00\x00')
    assert tested_lamp.state == StateLamp.OFF
    assert tested_lamp.color == b'\x34\x56\x78'

    tested_lamp.execute_cmd(b'\x12\x00\x00')
    assert tested_lamp.state == StateLamp.ON
    assert tested_lamp.color == b'\x34\x56\x78'

    tested_lamp.execute_cmd(b'\x13\x00\x00')
    assert tested_lamp.state == StateLamp.OFF
    assert tested_lamp.color == b'\x34\x56\x78'

    tested_lamp.execute_cmd(b'\x20\x00\x03\x9a\xbc\xde')
    assert tested_lamp.state == StateLamp.OFF
    assert tested_lamp.color == b'\x9a\xbc\xde'

    tested_lamp.execute_cmd(b'\x12\x00\x00')
    assert tested_lamp.state == StateLamp.ON
    assert tested_lamp.color == b'\x9a\xbc\xde'


def test_lamp_execute_cmd_fail():
    tested_lamp = Lamp()
    tested_lamp.execute_cmd(b'\x12\x00\x01')
    assert tested_lamp.state == StateLamp.OFF
    assert tested_lamp.color == b'\x00\x00\x00'

    tested_lamp.execute_cmd(b'\x12\x00\x01\x00')
    assert tested_lamp.state == StateLamp.OFF
    assert tested_lamp.color == b'\x00\x00\x00'

    tested_lamp.execute_cmd(b'\x20\x00\x02\x9a\xbc')
    assert tested_lamp.state == StateLamp.OFF
    assert tested_lamp.color == b'\x00\x00\x00'

    tested_lamp.execute_cmd(b'\x21\x00\x03\x9a\xbc\xde')
    assert tested_lamp.state == StateLamp.OFF
    assert tested_lamp.color == b'\x00\x00\x00'

    tested_lamp.execute_cmd(b'\x12\x00\x00')
    assert tested_lamp.state == StateLamp.ON
    assert tested_lamp.color == b'\x00\x00\x00'

    tested_lamp.execute_cmd(b'\x13\x00')
    assert tested_lamp.state == StateLamp.ON
    assert tested_lamp.color == b'\x00\x00\x00'

    tested_lamp.execute_cmd(b'\x13\x00\x01')
    assert tested_lamp.state == StateLamp.ON
    assert tested_lamp.color == b'\x00\x00\x00'

    tested_lamp.execute_cmd(b'\x13\x00\x01\x00')
    assert tested_lamp.state == StateLamp.ON
    assert tested_lamp.color == b'\x00\x00\x00'

    tested_lamp.execute_cmd(b'')
    assert tested_lamp.state == StateLamp.ON
    assert tested_lamp.color == b'\x00\x00\x00'
