import json
import logging
from datetime import timedelta, datetime
from typing import Any

import aiofiles
import aiohttp
import asyncio
from aiohttp import web

import settings
from enums import Endpoint

logger = logging.getLogger(__name__)


async def write_to_file(filename: str, data: dict[str, Any]) -> None:
    try:
        async with aiofiles.open(filename, 'a') as file:
            await file.write(json.dumps(data) + '\n')
    except Exception as e:
        logger.error(e)


async def get_statistics() -> str:
    try:
        async with aiohttp.ClientSession() as session:
            url = f'http://{settings.APP_HOST}:{settings.APP_PORT}{Endpoint.STATISTICS.value}'
            logging.info(f'request GET by {url=}')
            async with session.get(url=url) as response:
                logging.info(f'got {response=}')
                statistics = await response.text()
                return statistics
    except Exception as e:
        logger.error(e)


async def get_data_periodically(interval: timedelta) -> None:
    while True:
        statistics = await get_statistics()
        await write_to_file(
            filename=settings.STATISTICS_FILE_NAME,
            data={'statistics': statistics, 'timestamp': str(datetime.utcnow())}
        )
        await asyncio.sleep(delay=interval.total_seconds())


async def ping(request: web.Request) -> web.Response:
    return web.Response(status=200, text='ping')


async def start_background_tasks(app: web.Application) -> None:
    app['background_task'] = asyncio.create_task(
        get_data_periodically(interval=timedelta(seconds=settings.GET_STATISTICS_DELAY))
    )


async def cleanup_background_tasks(app: web.Application) -> None:
    app['background_task'].cancel()
    await app['background_task']
    app['background_task'] = None


if __name__ == '__main__':
    app = web.Application()
    app.router.add_get(Endpoint.PING.value, ping)
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    web.run_app(app)
