from typing import Callable, Coroutine

async def attempt(
        times: int,
        func: Callable[..., Coroutine],
        *,
        args: tuple = (),
        kwargs:dict = {},
        ):
    result = None
    exception = Exception()
    
    for _ in range(times):
        try:
            result = await func(*args, **kwargs)
        except Exception as e:
            exception = e
        else:
            return result

    raise exception