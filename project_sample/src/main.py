from aiohttp_lamp.client import WSClient
from aiohttp_lamp.lamp import Lamp
from settings import DEBUG, SERVER_HOST, SERVER_PORT


if __name__ == '__main__':
    my_lamp = Lamp(debug=DEBUG)
    ws_client = WSClient(server_host=SERVER_HOST, server_port=SERVER_PORT, lamp=my_lamp)
    ws_client.run()
