from typing import Any

import ujson


def json_dumps(data: dict[Any, Any]) -> str:
    return ujson.dumps(data, ensure_ascii=False)


def json_loads(data: str) -> dict[Any, Any]:
    return ujson.loads(data)
