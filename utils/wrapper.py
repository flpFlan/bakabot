import time, inspect
from collections import defaultdict

time_graph = defaultdict(lambda: 0.0)


def timecooling(seconds: float):
    def wrapper(func):
        async def _cfunc(*args, **kwargs):
            now_time = time.time()
            if now_time - time_graph[func] <= seconds:
                return
            time_graph[func] = now_time
            await func(*args, **kwargs)

        def _func(*args, **kwargs):
            now_time = time.time()
            if now_time - time_graph[func] <= seconds:
                return
            time_graph[func] = now_time
            func(*args, **kwargs)

        if inspect.iscoroutinefunction(func):
            return _cfunc
        else:
            return _func

    return wrapper
