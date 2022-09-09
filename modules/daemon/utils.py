import asyncio
from threading import Thread
from typing import Callable, Union
from time import time
import inspect

def run_async_thread(function: Callable) -> Thread:
    def inner():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(function())
        loop.close()

    thread = Thread(target=inner, daemon=True)
    thread.start()
    return thread

