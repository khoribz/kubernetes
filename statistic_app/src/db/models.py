from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.common.enums import Endpoint, Method


class Base(DeclarativeBase):
    pass


class Request(Base):
    __tablename__ = 'request'

    id: Mapped[int] = mapped_column(primary_key=True)
    endpoint: Mapped[Endpoint] = mapped_column(String)
    method: Mapped[Method] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
