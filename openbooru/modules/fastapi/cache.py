from fastapi_cache import FastAPICache
from fastapi_cache.coder import PickleCoder
from fastapi_cache.backends.inmemory import InMemoryBackend

def initialise_fastapi_cache():
    FastAPICache.init(InMemoryBackend(), coder=PickleCoder)