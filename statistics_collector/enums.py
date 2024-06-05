from enum import Enum


class Endpoint(str, Enum):
    PING = '/ping'
    STATISTICS = '/api/v1/statistics'