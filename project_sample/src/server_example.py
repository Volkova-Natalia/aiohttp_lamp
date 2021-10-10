from aiohttp import web, WSMsgType
import asyncio
from settings import SERVER_HOST, SERVER_PORT


async def ws_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    await asyncio.sleep(3)
    await ws.send_str('Hello, client!')

    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x55\x77\xff\xaa')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x12')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x13')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x20')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x12\x01')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x13\x01')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x20\x01')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x12\x00\xaa')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x13\x00\xaa')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x20\x03')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x20\x03\xaa')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x20\x03\xaa\xaa\xaa\xaa')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x12\x00')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x13\x00')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x20\x03\xaa\xbb\xcc')

    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x12\x00\x01')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x12\x00\x01\xaa')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x12\x01\x00')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x12\x01\x00\xaa')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x12\x00\x00\xaa')

    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x13\x00\x01')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x13\x00\x01\xaa')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x13\x01\x00')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x13\x01\x00\xaa')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x13\x00\x00\xaa')

    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x20\x03\x00\xaa\xbb\xcc')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x20\x00\x03\xaa\xbb')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x20\x00\x03\xaa\xbb\xcc\xdd')

    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x12\x00\x00')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x13\x00\x00')
    await asyncio.sleep(0.1)
    await ws.send_bytes(b'\x20\x00\x03\xaa\xbb\xcc')

    return ws


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([web.get('/', ws_handler)])
    web.run_app(app, host=SERVER_HOST, port=SERVER_PORT)
