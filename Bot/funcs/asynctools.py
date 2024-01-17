from functools import partial, wraps
from concurrent.futures import ThreadPoolExecutor
from asyncio import run_coroutine_threadsafe, gather

from Bot import user, bot, logger, user_loop, bot_loop

THREADPOOL = ThreadPoolExecutor(max_workers=1000)

def new_task(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return user_loop.create_task(function(*args, **kwargs))
    
    return wrapper

async def sync_to_async(function, *args, wait=True, **kwargs):
    pfunction = partial(function, *args, **kwargs)
    future = user_loop.run_in_executor(THREADPOOL, pfunction)
    return await future if wait else future

async def syncs_to_asyncs(*functions, wait=True):
    async_futures = []

    for function, *args in functions:
        pfunction = partial(function, *args)
        future = user_loop.run_in_executor(THREADPOOL, pfunction)
        async_futures.append(future)

    return await gather(*async_futures) if wait else async_futures
