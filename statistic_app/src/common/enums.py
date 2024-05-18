from enum import Enum


class Endpoint(str, Enum):
    GET_CURRENT_TIME = '/api/v1/time'
    GET_STATISTICS = '/api/v1/statistics'
    PING = '/ping/app'


class Method(str, Enum):
    GET = 'GET'
