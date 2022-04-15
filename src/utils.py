from functools import wraps

from fastapi.concurrency import run_in_threadpool


def run_async(f):
    @wraps(f)
    async def wrapped(*args, **kwargs):
        return await run_in_threadpool(f, *args, **kwargs)

    return wrapped
