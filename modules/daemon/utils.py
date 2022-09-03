import asyncio
from threading import Thread
from typing import Callable
from datetime import timedelta
from time import time


def schedule_task(function: Callable, time_between_runs:timedelta):
    def inner():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        schedule_function = scheduler(function, time_between_runs)
        loop.run_until_complete(schedule_function)
        loop.close()
    
    Thread(target=inner, daemon=True).start()


async def scheduler(func: Callable, time_between_runs:timedelta):
    last_run = 0
    while True:
        next_run_time = last_run + time_between_runs.total_seconds()
        time_til_next_run = next_run_time - time()
        await asyncio.sleep(time_til_next_run)
        last_run = time()
        await func()
