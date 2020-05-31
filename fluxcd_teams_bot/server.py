import logging
import aiohttp
from aiohttp import web, WSMsgType
from aiohttp.http_websocket import WSMessage

from fluxcd_teams_bot import settings
from fluxcd_teams_bot.parser import parse

logging.basicConfig(level=logging.DEBUG)


async def post_v6_events(request: web.Request) -> web.Response:
    # TODO check token

    data = await request.json()
    print(f'Got request: {data}')

    # Parse through json object to see if its useful
    if result := parse(data):
        async with aiohttp.ClientSession() as sesh:
            response = result.render()
            print(f'Sending response: {response}')
            async with sesh.post(settings.TEAMS_WEBHOOK, json=response) as resp:
                print(f'Webhook response code: {resp.status}')

    return web.Response(status=201)


async def ws_v11_daemon(request: web.Request) -> web.WebSocketResponse:
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:  # type: WSMessage
        if msg.type in (WSMsgType.TEXT, WSMsgType.BINARY):
            print(msg.data)
        elif msg.type == WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws


app = web.Application()
app.add_routes([
    web.get('/', ws_v11_daemon),
    web.get('/v11/daemon', ws_v11_daemon),
    web.post('/v6/events', post_v6_events)
])

if __name__ == '__main__':
    web.run_app(host=settings.LISTEN_ADDR, port=settings.LISTEN_PORT, app=app)
