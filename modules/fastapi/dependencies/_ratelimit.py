import time
from fastapi import Request, HTTPException, status

TIMEUNIT_LOOKUP = {
    "second":1,
    "minute":60,
    "hour":60*60,
    "day":60*60*24,
}

class RateLimit:
    events:dict[str,list[float]]
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
            raise ValueError("Bad Ratelimit String")

        if per_timeunit not in TIMEUNIT_LOOKUP:
            raise ValueError("Bad TimeUnit")

        if not limit.isdigit():
            raise ValueError("Bad Per Value")
        
        self.limit = int(limit)
        self.per = TIMEUNIT_LOOKUP[per_timeunit]
        self.events = {}


    def __call__(self,request: Request):
        ip = request.client.host #type: ignore

        if ip not in self.events:
            self.events[ip] = []
        
        if self.isBlocked(ip):
            raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS)
        else:
            self.events[ip].append(time.time())
        

    def isBlocked(self,key:str):
        since = time.time() - self.per

        accesses = 0
        for event in self.events[key]:
            if event < since:
                self.events[key].remove(event)
            else:
                accesses += 1

        if accesses >= self.limit:
            return True
        else:
            return False
