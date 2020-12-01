import logging

import aiohttp
from aiohttp import WSMsgType, web
from aiohttp.http_websocket import WSMessage
from pythonjsonlogger.jsonlogger import JsonFormatter

from fluxcd_teams_bot import settings
from fluxcd_teams_bot.parser import parse

# TODO move loggers to separate file
main_logger = logging.getLogger("flux2teams")
main_logger.setLevel(settings.LOG_LEVEL)
main_handler = logging.StreamHandler()
main_handler.setFormatter(
    JsonFormatter(
        fmt="%(levelname)s %(name)s %(pathname)s %(lineno)s %(message)s",
        rename_fields={
            "levelname": "level",
            "name": "logger",
            "pathname": "file",
        },
        timestamp=True,
    )
)
main_logger.addHandler(main_handler)
logger = logging.getLogger("flux2teams.server")

# TODO needs work, dont like the output
http_logger = logging.getLogger("flux2teams.http")
http_logger.propagate = False
http_handler = logging.StreamHandler()
http_handler.setFormatter(
    JsonFormatter(
        fmt="%(levelname)s %(name)s",
        rename_fields={
            "levelname": "level",
            "name": "logger"
        },
        timestamp=True,
    )
)
http_logger.addHandler(http_handler)


async def post_v6_events(request: web.Request) -> web.Response:
    # TODO check token

    data = await request.json()
    logger.debug(f"Got v6_events request: {data}")

    # Parse through json object to see if its useful
    if result := parse(data):
        async with aiohttp.ClientSession() as sesh:
            response = result.render()
            logger.info("Sending request to Teams")
            logger.debug(f"Request payload: {response}")
            async with sesh.post(settings.TEAMS_WEBHOOK, json=response) as resp:
                logger.debug(f"Webhook response code: {resp.status}")

    return web.Response(status=201)


async def ws_v11_daemon(request: web.Request) -> web.WebSocketResponse:
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:  # type: WSMessage
        if msg.type in (WSMsgType.TEXT, WSMsgType.BINARY):
            logger.debug(f"Webhook data: {msg.data}")
        elif msg.type == WSMsgType.ERROR:
            logger.exception("Caught websocket error", exc_info=ws.exception())

    logger.debug("Websocket closed")
    return ws


async def get_healthz(request: web.Request) -> web.Response:
    return web.Response(status=204)


app = web.Application()
app.add_routes(
    [web.get("/", ws_v11_daemon), web.get("/v11/daemon", ws_v11_daemon), web.post("/v6/events", post_v6_events), web.get("/healthz", get_healthz)]
)

if __name__ == "__main__":
    logger.info(f"Running server on {settings.LISTEN_ADDR}:{settings.LISTEN_PORT}")

    def _print(*args, **kwargs) -> None:
        return None

    web.run_app(host=settings.LISTEN_ADDR, port=settings.LISTEN_PORT, app=app, print=_print, access_log=http_logger)
