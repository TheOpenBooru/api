from pathlib import Path
from . import run_async_thread
import inspect
import asyncio
from time import time
from typing import Callable, Union
import pickledb

DB_PATH = Path("./data/tasks.json")
try:
    db = pickledb.load(DB_PATH, False)
except Exception:
    DB_PATH.unlink()
    db = pickledb.load(DB_PATH, False)


def create_background_task(
        id:str,
        function: Callable,
        retry_after:Union[float,None] = None
    ):
    Task(id,function,retry_after).start()


class Task:
    isAsync: bool
    id: str
    function: Callable
    retry_after: int|float|None
    last_run: int|float = 0.0
    running: bool = False
    
    
    def __init__(self,
            id:str,
            function: Callable,
            retry_after:Union[float,None] = None
        ):
        self.id = id
        self.function = function
        self.isAsync = inspect.iscoroutinefunction(function)
        self.retry_after = retry_after
        if db.exists(id):
            self.last_run = float(db.get(id))


    def start(self):
        async def thread_target():
            if self.retry_after == None:
                await self._run_function()
                self.stop()
            else:
                await self._scheduler()
        
        self._thread = run_async_thread(thread_target)


    def stop(self):
        self.running = False
        self._thread.join()


    async def _scheduler(self):
        assert self.retry_after != None
        
        while True:
            next_run_time = self.last_run + self.retry_after
            time_til_next_run = next_run_time - time()
            await asyncio.sleep(time_til_next_run)
            await self._run_function()
            self._update_last_run()
            
            if self.running == False:
                break


    def _update_last_run(self):
        cur_time = time()
        self.last_run = cur_time
        db.set(self.id, str(int(cur_time)))


    async def _run_function(self):
        if self.isAsync:
            await self.function()
        else:
            self.function()

