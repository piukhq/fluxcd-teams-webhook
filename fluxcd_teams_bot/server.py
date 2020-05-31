
from aiohttp import web, WSMsgType
from aiohttp.http_websocket import WSMessage
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity

from fluxcd_teams_bot import settings
from fluxcd_teams_bot.bot_adapter import BOT_ADAPTER
from fluxcd_teams_bot.bot import Bot
from fluxcd_teams_bot.parser import parse


routes = web.RouteTableDef()

BOT = Bot()


# Teams webhook
@routes.post('/api/messages')
async def post_api_messages(request: web.Request) -> web.Response:
    if 'application/json' not in request.headers['Content-Type']:
        return web.Response(status=415)

    body = await request.json()
    activity = Activity().deserialize(body)
    auth_header = request.headers.get('Authorization', '')

    response = web.Response(status=201)
    if response_data := await BOT_ADAPTER.process_activity(activity, auth_header, BOT.on_turn):
        response = web.json_response(data=response_data.body, status=response_data.status)

    return response


@routes.post('/v6/events')
async def post_v6_events(request: web.Request) -> web.Response:
    # TODO check token

    data = await request.json()

    # Parse through json object to see if its useful
    if result := parse(data):
        # TODO make this a queue, as send_activity takes ages
        await BOT.send_activity(result)

    return web.Response(status=201)


@routes.get('/v11/daemon')
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


app = web.Application(middlewares=[aiohttp_error_middleware])
app.router.add_routes(routes)

if __name__ == '__main__':
    web.run_app(host=settings.LISTEN_ADDR, port=settings.LISTEN_PORT, app=app)
