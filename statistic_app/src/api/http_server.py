import logging
from datetime import datetime

from aiohttp import web

from src.common.enums import Endpoint, Method
from src.db.manager import DBManager

logger = logging.getLogger(__name__)


class HTTPServer:
    def __init__(self, db_manager: DBManager) -> None:
        self._db_manager = db_manager

        external_app = web.Application()
        external_app.router.add_get(Endpoint.GET_CURRENT_TIME.value, self.get_current_time)
        external_app.router.add_get(Endpoint.GET_STATISTICS.value, self.get_statistics)

        internal_app = web.Application()
        internal_app.router.add_get(Endpoint.PING.value, self.ping)

        self._external_app = external_app
        self._internal_app = internal_app

    @property
    def external_app(self) -> web.Application:
        return self._external_app

    @property
    def internal_app(self) -> web.Application:
        return self._internal_app

    @property
    def db_manager(self) -> DBManager:
        return self._db_manager

    async def ping(self, _: web.Request) -> web.Response:
        logger.debug('healthcheck request')
        status_code = 200
        if not await self._db_manager.healthcheck():
            status_code = 500

        if status_code == 200:
            logger.debug(f'healthcheck response with {status_code}')
        else:
            logger.error(f'healthcheck response with {status_code}')

        return web.Response(status=status_code)

    async def get_current_time(self, request: web.Request) -> web.Response:
        current_time = datetime.utcnow()
        await self.db_manager.insert_request(
            method=request.method,
            endpoint=request.path,
            created_at=current_time
        )
        return web.Response(status=200, body=str(current_time))

    async def get_statistics(self, request: web.Request) -> web.Response:
        await self.db_manager.insert_request(
            method=request.method,
            endpoint=request.path,
            created_at=datetime.utcnow()
        )
        time_requests_count = await self.db_manager.get_requests_count(
            method=Method.GET,
            endpoint=Endpoint.GET_CURRENT_TIME,
        )
        return web.Response(status=200, body=str(time_requests_count))
