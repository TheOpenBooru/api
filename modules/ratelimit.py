from collections import defaultdict
from dataclasses import dataclass
import time


class RateLimitException(Exception):
    until: float
    def __init__(self, until:float):
        self.until = until
        ...


Actions:dict[str, list[float]] = defaultdict(list)
def ratelimit(id:str, limit:str):
    """
    Provide a string in the format `per`/`TimeUnit`
    Example:
    - 5/day
    - 1/second

    Valid Units:
    - second
    - minute
    - hour
    - day

    Raises:
    - RateLimitException
    """
    now = time.time()
    
    per, timeinterval = _parseString(limit)
    recentActions = Actions[id]

    def filterFunc(event: float):
        time_since = now - event
        return time_since < timeinterval
    
    recentActions = list(filter(filterFunc, recentActions))
    
    if len(recentActions) > per:
        historic_action = min(recentActions)
        time_remaining = (now - historic_action - timeinterval)
        raise RateLimitException(time_remaining)
    else:
        Actions[id].append(now)


def _parseString(string:str) -> tuple[int, float]:
    TIMEUNIT_LOOKUP = {
        "second":1,
        "minute":60,
        "hour":60*60,
        "day":60*60*24,
    }
    
    try:
        limit,per_timeunit = string.split("/")
    except Exception:
        raise RuntimeError("Bad Ratelimit String")

    if per_timeunit not in TIMEUNIT_LOOKUP:
        raise RuntimeError("Bad TimeUnit")

    if not limit.isdigit():
        raise RuntimeError("Bad Per Value")
    
    return int(limit), TIMEUNIT_LOOKUP[per_timeunit]
