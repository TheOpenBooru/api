from fastapi_cache import FastAPICache
from fastapi_cache.coder import PickleCoder
from fastapi_cache.backends.inmemory import InMemoryBackend

def cache_init():
    FastAPICache.init(InMemoryBackend(), coder=PickleCoder)