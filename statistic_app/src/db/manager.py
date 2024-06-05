import logging
import subprocess
from contextlib import asynccontextmanager, AsyncExitStack
from datetime import datetime
from typing import AsyncIterator

from sqlalchemy import text, insert, select, func
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import _AsyncSessionContextManager, AsyncSession
from sqlalchemy.orm import close_all_sessions

from src.common.enums import Method, Endpoint
from src.common.helpers import json_dumps, json_loads
from src.db.models import Request

logger = logging.getLogger(__name__)


class DBManager:
    def __init__(self, async_engine: AsyncEngine):
        self._async_engine = async_engine
        self._async_session = async_sessionmaker(
            self._async_engine,
            expire_on_commit=False,
        )

    async def healthcheck(self) -> bool:
        try:
            async with self.session() as session:
                result = await session.execute(text('CREATE TEMPORARY TABLE temp (id INTEGER) ON COMMIT DROP;'))
                return result.connection.connection.is_valid  # type: ignore
        except Exception:
            logger.exception('db healthcheck failed')
            return False

    def session(self) -> _AsyncSessionContextManager[AsyncSession]:
        return self._async_session.begin()

    @asynccontextmanager
    async def use_or_create_session(
        self,
        current_session: AsyncSession | None,
    ) -> AsyncIterator[AsyncSession]:
        async with AsyncExitStack() as stack:
            if current_session is None:
                session = await stack.enter_async_context(self.session())
            else:
                session = current_session

            yield session

    async def close(self) -> None:
        close_all_sessions()
        await self._async_engine.dispose()

    async def insert_request(
        self,
        method: str | Method,
        endpoint: str | Endpoint,
        created_at: datetime,
        current_session: AsyncSession | None = None,
    ) -> int:
        async with self.use_or_create_session(current_session) as session:
            return await session.execute(
                insert(Request)
                .values(
                    method=method,
                    endpoint=endpoint,
                    created_at=created_at,
                )
                .returning(Request)
            )

    async def get_requests_count(
        self,
        method: str | Method,
        endpoint: str | Endpoint,
        current_session: AsyncSession | None = None,
    ) -> int:
        async with self.use_or_create_session(current_session) as session:
            requests_count = await session.scalar(
                select(func.count())
                .select_from(Request)
                .where(
                    Request.method == method,
                    Request.endpoint == endpoint,
                )
            )
            return requests_count or 0


def init_db_manager(
    str_for_connect: str,
    run_migrations: bool = True,
) -> DBManager:
    engine = create_async_engine(
        str_for_connect,
        pool_pre_ping=True,
        json_serializer=json_dumps,
        json_deserializer=json_loads,
    )
    if run_migrations:
        subprocess.run('alembic upgrade head', check=True, shell=True)
    return DBManager(engine)
