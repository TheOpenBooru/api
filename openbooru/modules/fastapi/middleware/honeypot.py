from openbooru.modules import blacklist, settings
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Response, Request
from pathlib import Path

URLS_PATH = Path("./data/blocked_urls.txt")
if URLS_PATH.exists():
    blocked_urls = set(URLS_PATH.read_text().split("\n"))
else:
    blocked_urls = set()

class HoneypotMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.scope.get("path", "/")
        if settings.USE_HONEYPOT and path in blocked_urls:
            if request.client:
                blacklist.ban(request.client.host, f"Tried to access {path}")

        response = await call_next(request)
        return response
