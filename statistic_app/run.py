import asyncio
import logging
from typing import Callable, Awaitable

import uvloop
from aiohttp import web

import settings
from src.api.http_server import HTTPServer
from src.db.manager import init_db_manager

logger = logging.getLogger(__name__)


def on_shutdown_wrapper(coroutine: Callable[..., Awaitable]) -> Callable[..., Awaitable]:
    """
    Wrapper to run on_cleanup coroutines without aiohttp app argument.
    """
    async def skip_app_wrapper(_):
        await coroutine()

    return skip_app_wrapper


async def get_http_server() -> HTTPServer:
    logger.info('create db manager')
    db_manager = init_db_manager(str_for_connect=settings.POSTGRES_STR_FOR_CONNECT)

    http_server = HTTPServer(db_manager=db_manager)
    http_server.external_app.on_shutdown.extend(
        [
            on_shutdown_wrapper(db_manager.close),
        ],
    )

    return http_server


async def start_server(app: web.Application, port: int, runners: list[web.AppRunner]):
    logger.info(f'starting http server on {port=}')
    runner = web.AppRunner(app, handle_signals=True)
    runners.append(runner)
    await runner.setup()
    site = web.TCPSite(runner, settings.APP_HOST, port)
    await site.start()


if __name__ == '__main__':
    logger.info('set event loop as uvloop')
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    loop = asyncio.get_event_loop()
    http_server = loop.run_until_complete(get_http_server())

    logger.info('start http server')
    runners = []
    loop.create_task(start_server(app=http_server.internal_app, port=settings.INTERNAL_PORT, runners=runners))
    loop.create_task(start_server(app=http_server.external_app, port=settings.EXTERNAL_PORT, runners=runners))

    try:
        loop.run_forever()
    except Exception:
        pass
    finally:
        logger.info('stop servers')
        for runner in runners:
            loop.run_until_complete(runner.cleanup())