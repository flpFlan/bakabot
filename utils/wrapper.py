# -- stdlib --
import time, inspect
from collections import defaultdict
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Literal, Optional, overload

# -- third party --
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# -- code --
if TYPE_CHECKING:
    from datetime import datetime, tzinfo
    from services.base import Service

time_graph: defaultdict[Callable, float] = defaultdict(lambda: 0.0)


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
    _scheduler.start()

    class _Trigger:
        trigger: ClassVar[str]

        @overload
        def __init__(self, refer: "Service", **kwargs):
            ...

        @overload
        def __init__(self, refer: None = None, *, forget: Literal[True], **kwargs):
            ...

        def __init__(
            self, refer: Optional["Service"] = None, *, forget=False, **kwargs
        ):
            if not forget:
                assert refer is not None
                self.refer = refer
            self.forget = forget
            self._args = {} | kwargs

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            ...

        def add(self, f: Callable):
            job = Scheduled._scheduler.add_job(f, self.__class__.trigger, **self._args)
            if not self.forget:

                async def pause():
                    job.pause()

                async def resume():
                    job.resume()

                self.refer.OnBeforeShutDown += pause
                self.refer.OnAfterStart += resume
            return job

        def timezone(self, t: "tzinfo | str"):
            self._args["timezone"] = t
            return self

        def args(self, *args: Any):
            self._args["args"] = args
            return self

    class Interval(_Trigger):
        """固定时间间隔触发"""

        trigger = "interval"

        def weeks(self, t: int):
            self._args["weeks"] = t
            return self

        def days(self, t: int):
            self._args["days"] = t
            return self

        def hours(self, t: int):
            self._args["hours"] = t
            return self

        def minutes(self, t: int):
            self._args["minutes"] = t
            return self

        def seconds(self, t: int):
            self._args["seconds"] = t
            return self

        def start_date(self, t: "datetime | str"):
            self._args["start_date"] = t
            return self

        def end_date(self, t: "datetime | str"):
            self._args["end_date"] = t
            return self

    class Crontab(_Trigger):
        """特定时间点触发"""

        trigger = "cron"

        def year(self, t: int | str):
            self._args["year"] = t
            return self

        def month(self, t: int | str):
            self._args["month"] = t
            return self

        def day(self, t: int | str):
            self._args["day"] = t
            return self

        def week(self, t: int | str):
            self._args["week"] = t
            return self

        def day_of_week(self, t: int | str):
            self._args["day_of_week"] = t
            return self

        def hour(self, t: int | str):
            self._args["hour"] = t
            return self

        def minute(self, t: int | str):
            self._args["minute"] = t
            return self

        def second(self, t: int | str):
            self._args["second"] = t
            return self

        def start_date(self, t: "datetime | str"):
            self._args["start_date"] = t
            return self

        def end_date(self, t: "datetime | str"):
            self._args["end_date"] = t
            return self

    class Date(_Trigger):
        """特定时间点触发(只触发一次)"""

        trigger = "date"

        def run_date(self, t: "datetime | str"):
            self._args["run_date"] = t
            return self
