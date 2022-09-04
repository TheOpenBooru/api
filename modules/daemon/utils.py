import asyncio
from threading import Thread
from typing import Callable, Union
from datetime import timedelta
from time import time


def run_async_thread(function: Callable):
    def inner():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(function())
        loop.close()
    Thread(target=inner, daemon=True).start()


def schedule_task(function:Callable, time_between_runs:Union[None, float]):
    async def inner():
        if time_between_runs == None:
            await function()
        else:
            await scheduler(function, time_between_runs)
    
    run_async_thread(inner)


async def scheduler(func:Callable, time_between_runs:float):
    last_run = 0
    while True:
        next_run_time = last_run + time_between_runs
        time_til_next_run = next_run_time - time()
        await asyncio.sleep(time_til_next_run)
        last_run = time()
        await func()
