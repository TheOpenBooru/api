from . import GetAccount
import time
from fastapi import Request, HTTPException, status, Depends

TIMEUNIT_LOOKUP = {
    "second":1,
    "minute":60,
    "hour":60*60,
    "day":60*60*24,
}

class RateLimit:
    events:dict[int, list[float]]
    limit:int
    per:int

    def __init__(self, limit:str):
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
        """
        try:
            limit,per_timeunit = limit.split("/")
        except Exception:
            raise RuntimeError("Bad Ratelimit String")

        if per_timeunit not in TIMEUNIT_LOOKUP:
            raise RuntimeError("Bad TimeUnit")

        if not limit.isdigit():
            raise RuntimeError("Bad Per Value")
        
        self.limit = int(limit)
        self.per = TIMEUNIT_LOOKUP[per_timeunit]
        self.events = {}


    def __call__(self, request: Request, account: GetAccount = Depends()):
        id = account.id

        if id not in self.events:
            self.events[id] = []
        
        if self.isBlocked(id):
            time_left = time.time() - self.events[id][-1]
            retry_string = str(round(time_left,2))
            raise HTTPException(
                status.HTTP_429_TOO_MANY_REQUESTS,
                headers={"Retry-After": retry_string}
                )
        else:
            self.events[id].append(time.time())
        

    def isBlocked(self, id: int):
        since = time.time() - self.per

        accesses = 0
        for event in self.events[id]:
            if event < since:
                self.events[id].remove(event)
            else:
                accesses += 1

        if accesses >= self.limit:
            return True
        else:
            return False
