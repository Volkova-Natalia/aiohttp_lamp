from aiohttp import web
from aiohttp_lamp.client import WSClient
from aiohttp_lamp.lamp import Lamp, StateLamp
from aiohttp_lamp.commands.consts import CmdON, CmdOFF, CmdCOLOR
from aiohttp_lamp.commands.utils import create_cmd, create_cmd_ON, create_cmd_OFF, create_cmd_COLOR


# ------------------------------
ON_TYPE = CmdON.TYPE.value
ON_DATA_LENGTH = CmdON.DATA_LENGTH.value

OFF_TYPE = CmdOFF.TYPE.value
OFF_DATA_LENGTH = CmdOFF.DATA_LENGTH.value

COLOR_TYPE = CmdCOLOR.TYPE.value
COLOR_DATA_LENGTH = CmdCOLOR.DATA_LENGTH.value


class FakeWSServer:
    def __init__(self, host='0.0.0.0', port=0, send_messages=None):
        self.host = host
        self.port = port
        self.app = web.Application()
        self.app.add_routes([web.get('/', self.ws_handler)])
        self.runner = web.AppRunner(self.app)
        self.send_messages = send_messages

    async def start(self) -> None:
        await self.runner.setup()
        server = web.TCPSite(self.runner, host=self.host, port=self.port)
        await server.start()

    async def stop(self) -> None:
        await self.runner.cleanup()

    async def ws_handler(self, request) -> None:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        if self.send_messages:
            await self.send_messages(ws)
        return ws


async def common_test_pattern(send_messages, check_asserts) -> None:
    tested_lamp = Lamp()
    ws_client = WSClient(lamp=tested_lamp)
    fake_ws_server = FakeWSServer(host=ws_client.server_host, port=ws_client.server_port, send_messages=send_messages)
    await fake_ws_server.start()
    await ws_client.ws_handler()
    check_asserts(tested_lamp)
    await fake_ws_server.stop()
# ------------------------------


async def test_client_send_nothing() -> None:
    async def send_messages(ws) -> None:
        pass

    def check_asserts(tested_lamp):
        assert tested_lamp.state == StateLamp.OFF
        assert tested_lamp.color == b'\x00\x00\x00'

    await common_test_pattern(send_messages, check_asserts)


async def test_client_send_string() -> None:
    async def send_messages(ws) -> None:
        await ws.send_str('Hello, client!')

    def check_asserts(tested_lamp):
        assert tested_lamp.state == StateLamp.OFF
        assert tested_lamp.color == b'\x00\x00\x00'

    await common_test_pattern(send_messages, check_asserts)


async def test_client_send_invalid_msg() -> None:
    async def send_messages(ws) -> None:
        await ws.send_bytes(b'')
        await ws.send_bytes(b'\x00\x00\x00\x00\x00\x00\x00')
        await ws.send_bytes(ON_TYPE)
        await ws.send_bytes(create_cmd(ON_TYPE + OFF_TYPE + COLOR_TYPE, ON_DATA_LENGTH, b'\x34\x56\x78\x9a\xbc\xde'))
        await ws.send_bytes(create_cmd(ON_TYPE + OFF_TYPE + COLOR_TYPE, ON_DATA_LENGTH, b''))
        await ws.send_bytes(OFF_TYPE)
        await ws.send_bytes(create_cmd(ON_TYPE + OFF_TYPE + COLOR_TYPE, OFF_DATA_LENGTH, b'\x34\x56\x78\x9a\xbc\xde'))
        await ws.send_bytes(create_cmd(ON_TYPE + OFF_TYPE + COLOR_TYPE, OFF_DATA_LENGTH, b''))
        await ws.send_bytes(COLOR_TYPE)
        await ws.send_bytes(create_cmd(ON_TYPE + OFF_TYPE + COLOR_TYPE, COLOR_DATA_LENGTH, b'\x34\x56\x78\x9a\xbc\xde'))
        await ws.send_bytes(create_cmd(ON_TYPE + OFF_TYPE + COLOR_TYPE, COLOR_DATA_LENGTH, b'\x34\x56\x78'))
        await ws.send_bytes(create_cmd(COLOR_TYPE, COLOR_DATA_LENGTH, b''))
        await ws.send_bytes(create_cmd(COLOR_TYPE, COLOR_DATA_LENGTH, b'\x34\x56\x78\x9a'))

    def check_asserts(tested_lamp):
        assert tested_lamp.state == StateLamp.OFF
        assert tested_lamp.color == b'\x00\x00\x00'

    await common_test_pattern(send_messages, check_asserts)


async def test_client_send_valid_on() -> None:
    async def send_messages(ws) -> None:
        await ws.send_bytes(create_cmd_ON())

    def check_asserts(tested_lamp):
        assert tested_lamp.state == StateLamp.ON
        assert tested_lamp.color == b'\x00\x00\x00'

    await common_test_pattern(send_messages, check_asserts)


async def test_client_send_invalid_on() -> None:
    async def send_messages(ws) -> None:
        await ws.send_bytes(b'\x00\x00\x00')
        await ws.send_bytes(create_cmd(ON_TYPE + OFF_TYPE + COLOR_TYPE, ON_DATA_LENGTH, b''))
        await ws.send_bytes(create_cmd(ON_TYPE, ON_DATA_LENGTH + 1, b'\x34'))

    def check_asserts(tested_lamp):
        assert tested_lamp.state == StateLamp.OFF
        assert tested_lamp.color == b'\x00\x00\x00'

    await common_test_pattern(send_messages, check_asserts)


async def test_client_send_valid_off() -> None:
    async def send_messages(ws) -> None:
        await ws.send_bytes(create_cmd_ON())
        await ws.send_bytes(create_cmd_OFF())

    def check_asserts(tested_lamp):
        assert tested_lamp.state == StateLamp.OFF
        assert tested_lamp.color == b'\x00\x00\x00'

    await common_test_pattern(send_messages, check_asserts)


async def test_client_send_invalid_off() -> None:
    async def send_messages(ws) -> None:
        await ws.send_bytes(create_cmd_ON())
        await ws.send_bytes(b'\x00\x00\x00')
        await ws.send_bytes(create_cmd(ON_TYPE + OFF_TYPE + COLOR_TYPE, OFF_DATA_LENGTH, b''))
        await ws.send_bytes(create_cmd(OFF_TYPE, OFF_DATA_LENGTH + 1, b'\x34'))

    def check_asserts(tested_lamp):
        assert tested_lamp.state == StateLamp.ON
        assert tested_lamp.color == b'\x00\x00\x00'

    await common_test_pattern(send_messages, check_asserts)


async def test_client_send_valid_color() -> None:
    async def send_messages(ws) -> None:
        await ws.send_bytes(create_cmd_COLOR(b'\x34\x56\x78'))

    def check_asserts(tested_lamp):
        assert tested_lamp.state == StateLamp.OFF
        assert tested_lamp.color == b'\x34\x56\x78'

    await common_test_pattern(send_messages, check_asserts)


async def test_client_send_invalid_color() -> None:
    async def send_messages(ws) -> None:
        await ws.send_bytes(b'\x00\x00\x00')
        await ws.send_bytes(create_cmd(ON_TYPE + OFF_TYPE + COLOR_TYPE, COLOR_DATA_LENGTH, b'\x34\x56\x78'))
        await ws.send_bytes(create_cmd(COLOR_TYPE, COLOR_DATA_LENGTH + 1, b'\x34\x56\x78\x9a'))

    def check_asserts(tested_lamp):
        assert tested_lamp.state == StateLamp.OFF
        assert tested_lamp.color == b'\x00\x00\x00'

    await common_test_pattern(send_messages, check_asserts)
