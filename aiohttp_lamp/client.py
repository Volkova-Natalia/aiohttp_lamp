import aiohttp
import asyncio
from .lamp import Lamp


class WSClient:
    def __init__(self, server_host='127.0.0.1', server_port=9999, lamp=None):
        self.server_host = server_host
        self.server_port = server_port
        self.server = fr'http://{server_host}:{server_port}'
        self.lamp = lamp if lamp else Lamp()
        self.loop = asyncio.get_event_loop()

    def run(self) -> None:
        self.loop.run_until_complete(self.ws_handler())
        self.loop.run_until_complete(asyncio.sleep(0))
        self.loop.close()

    async def ws_handler(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(self.server) as ws:
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.ERROR:
                        break
                    elif msg.type == aiohttp.WSMsgType.BINARY:
                        self.lamp.execute_cmd(msg.data)
