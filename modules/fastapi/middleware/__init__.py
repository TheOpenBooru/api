from .blacklist import BlacklistMiddleware
from starlette.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

middlewares = [
    Middleware(BlacklistMiddleware),
    Middleware(GZipMiddleware),
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    ),
]
