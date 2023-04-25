# -- stdlib --
import asyncio
import logging
from typing import Type, cast
from re import compile

# -- third party --
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler

# -- own --
from config import Bots

# -- code --

log = logging.getLogger("bot.service")


class ServiceCore:
    core_on = False

    def __init__(self, service):
        from bot import Bot

        self.service = service
        self.bot = getattr(self, "bot", None) or cast(Bot, None)
        if isinstance(self, IMessageFilter):
            IMessageFilter.__init__(self)

    def run(self):
        self.core_on = True

    def close(self):
        self.core_on = False


class EventHandler(ServiceCore):
    from cqhttp.base import Event

    interested: list[Type[Event]]

    async def handle(self, evt: Event):
        ...  # to override it


class IMessageFilter:
    from cqhttp.events.message import Message

    entrys = []
    entry_flags = 0

    def __init__(self):
        entry = self.entrys
        self.entrys = [compile(et, self.entry_flags) for et in entry]

    def filter(self, evt: Message):
        msg = evt.message
        for _entry in self.entrys:
            if match := _entry.match(msg):
                return match.groupdict()


class SheduledHandler(ServiceCore):
    shedule_trigger: str
    args: dict

    def run(self):
        super().run()
        self.jobs = jobs = []
        self.scheduler = scheduler = BackgroundScheduler()  # AsyncIOScheduler()
        if self.shedule_trigger == "interval":
            jobs.append(
                scheduler.add_job(
                    lambda: asyncio.run(self.handle()), "interval", **self.args
                )
            )
        if self.shedule_trigger == "cron":
            jobs.append(
                scheduler.add_job(
                    lambda: asyncio.run(self.handle()), "cron", **self.args
                )
            )
        scheduler.start()

    def close(self):
        super().close()
        self.scheduler.remove_all_jobs()
        self.jobs = []

    async def handle(self):
        ...


class Service:
    priority = 3
    service_on = False
    cores = []
    execute_before = []
    execute_after = []

    def __init__(self, bot):
        from bot import Bot

        self.bot = bot = cast(Bot, bot)
        self.cores = [core(self) for core in self.cores]  # type: ignore
        self.cores = cast(list[ServiceCore], self.cores)
        for core in self.cores:
            core.bot = bot

    async def start(self):
        bot = self.bot
        db = bot.db
        service = self.__class__.__name__
        db.execute(
            """
            insert or replace into services (service,service_on) values (?,?)
            """,
            (service, True),
        )
        db.commit()
        for core in self.cores:
            core.run()
        self.service_on = True

    async def close(self):
        bot = self.bot
        db = bot.db
        service = self.__class__.__name__

        db.execute(
            "insert or replace into services (service,service_on) values (?,?)",
            (service, False),
        )
        db.commit()
        for core in self.cores:
            core.close()
        self.service_on = False


def register_to(*bots):
    if "all" or "ALL" in bots:
        bots = [b.name for b in Bots]

    def register(cls):
        for b in Bots:
            if b.name in bots:
                b.services.append(cls)
        return cls

    def except_for(*_bots):
        include = [b for b in bots if b not in _bots]
        return register_to(include)

    register.except_for = except_for
    return register
