import asyncio
import threading
import time, inspect
from collections import defaultdict

time_graph = defaultdict(lambda: 0.0)


def cool_down_for(seconds: float):
    def wrapper(func):
        async def _cfunc(*args, **kwargs):
            now_time = time.time()
            if now_time - time_graph[func] <= seconds:
                return
            time_graph[func] = now_time
            return await func(*args, **kwargs)

        def _func(*args, **kwargs):
            now_time = time.time()
            if now_time - time_graph[func] <= seconds:
                return
            time_graph[func] = now_time
            return func(*args, **kwargs)

        if inspect.iscoroutinefunction(func):
            return _cfunc
        else:
            return _func

    return wrapper


def interval_scheduled(seconds: float, *args, **kwargs):
    def wrapper(func):
        if inspect.iscoroutinefunction(func):

            def _run_cfunc(f, *args, **kwargs):
                asyncio.run(f(*args, **kwargs))

            threading.Timer(seconds, _run_cfunc, func, *args, **kwargs).start()
        else:
            threading.Timer(function=func, interval=seconds, *args, **kwargs).start()
        return func

    return wrapper
