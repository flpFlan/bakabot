# -- stdlib --
from datetime import datetime, tzinfo
import time, inspect
from collections import defaultdict
from typing import Any, Callable, ClassVar, Coroutine

# -- third party --
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.job import Job

# -- own --
from utils.subevent import SubEvent

# -- code --

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


class Scheduled:
    _scheduler: ClassVar[AsyncIOScheduler] = AsyncIOScheduler()
    _jobs: ClassVar[dict[str, Job]] = {}

    @classmethod
    # TODO
    def cancel(cls, name: str):
        if name in cls._jobs:
            cls._jobs[name].remove()
            cls._jobs.pop(name)

    class __Trigger:
        trigger: ClassVar[str]

        def __init__(self, **kwargs):
            self.__args = {} | kwargs

        def add(self, f: Callable):
            job = Scheduled._scheduler.add_job(f, self.__class__.trigger, **self.__args)
            Scheduled._jobs[f.__name__] = job

        def timezone(self, t: tzinfo | str):
            self.__args["timezone"] = t
            return self

        def args(self, *args: Any):
            self.__args["args"] = args
            return self

    class Interval(__Trigger):
        """固定时间间隔触发"""

        trigger = "interval"

        def weeks(self, t: int):
            self.__args["weeks"] = t
            return self

        def days(self, t: int):
            self.__args["days"] = t
            return self

        def hours(self, t: int):
            self.__args["hours"] = t
            return self

        def minutes(self, t: int):
            self.__args["minutes"] = t
            return self

        def seconds(self, t: int):
            self.__args["seconds"] = t
            return self

        def start_date(self, t: datetime | str):
            self.__args["start_date"] = t
            return self

        def end_date(self, t: datetime | str):
            self.__args["end_date"] = t
            return self

    class Crontab(__Trigger):
        """特定时间点触发"""

        trigger = "cron"

        def year(self, t: int | str):
            self.__args["year"] = t
            return self

        def month(self, t: int | str):
            self.__args["month"] = t
            return self

        def day(self, t: int | str):
            self.__args["day"] = t
            return self

        def week(self, t: int | str):
            self.__args["week"] = t
            return self

        def day_of_week(self, t: int | str):
            self.__args["day_of_week"] = t
            return self

        def hour(self, t: int | str):
            self.__args["hour"] = t
            return self

        def minute(self, t: int | str):
            self.__args["minute"] = t
            return self

        def second(self, t: int | str):
            self.__args["second"] = t
            return self

        def start_date(self, t: datetime | str):
            self.__args["start_date"] = t
            return self

        def end_date(self, t: datetime | str):
            self.__args["end_date"] = t
            return self

    class Date(__Trigger):
        """特定时间点触发(只触发一次)"""

        trigger = "date"

        def run_date(self, t: datetime | str):
            self.__args["run_date"] = t
            return self
