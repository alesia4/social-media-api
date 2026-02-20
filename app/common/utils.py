from datetime import datetime, timezone
from typing import Tuple


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def clamp_pagination(limit: int, offset: int, max_limit: int = 50) -> Tuple[int, int]:
    if limit < 1:
        limit = 1
    if limit > max_limit:
        limit = max_limit
    if offset < 0:
        offset = 0
    return limit, offset
