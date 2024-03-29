from .blacklist import BlacklistMiddleware
from .honeypot import HoneypotMiddleware
from starlette.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

middlewares = [
    Middleware(BlacklistMiddleware),
    Middleware(HoneypotMiddleware),
    Middleware(GZipMiddleware),
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    ),
]
