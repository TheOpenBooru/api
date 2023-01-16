from modules import blacklist
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Response


class BlacklistMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.client and blacklist.check_blacklist(request.client.host):
            reason = blacklist.get_ban_reason(request.client.host)
            return Response(
                content="IP Banned: " + reason,
                status_code=403,
            )

        response = await call_next(request)
        return response
