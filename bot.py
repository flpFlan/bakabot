# -- stdlib --
import asyncio
from collections import defaultdict
import logging, os
import datetime
from typing import Type, cast

# -- third party --

# -- own --
from adapter import CQHTTPAdapter
from cqhttp.base import Event
from cqhttp.api.base import ApiAction
from cqhttp.events.base import CQHTTPEvent
from db.database import DataBase
from services.base import EventHandler, Service


# -- code --
log = logging.getLogger("bot")


def sort_services(services):
    graph = {}
    for seivice in services:
        graph[seivice] = {
            "before": set(seivice.execute_before),
            "after": set(seivice.execute_after),
        }
        for dep in seivice.execute_before:
            graph[dep]["after"].add(seivice)
        for dep_by in seivice.execute_after:
            graph[dep_by]["before"].add(seivice)

    queue = [service for service, dep in graph.items() if not dep["before"]]
    result = []
    while queue:
        service = queue.pop(0)
        result.append(service)
        for dep_by in graph[service]["after"]:
            graph[dep_by]["before"].remove(service)
            if not graph[dep_by]["before"]:
                queue.append(dep_by)

    for i, service in enumerate(result):
        for dep in service.execute_before:
            dep_idx = services.index(dep())
            if dep_idx >= i:
                services[i], services[dep_idx] = services[dep_idx], services[i]
                i = dep_idx
        for dep_by in service.execute_after:
            dep_by_index = services.index(dep_by())
            if dep_by_index <= i:
                services[dep_by_index], services[i] = (
                    services[i],
                    services[dep_by_index],
                )


class BotBehavior:
    def set_bot(self, bot):
        self.bot = cast(Bot, bot)

    async def process_evt(self, evt: Event):
        if isinstance(evt, CQHTTPEvent):
            ...
        elif isinstance(evt, ApiAction):
            ...
        else:
            pass

    # async def process_evt(self, evt: Event):
    #     for service in self.bot.services:
    #         if not service.service_on:
    #             continue
    #         from services.base import EventHandler

    #         for handler in service.cores:
    #             if not handler.core_on:
    #                 continue
    #             if not isinstance(handler, EventHandler):
    #                 continue
    #             if not self.is_interested(evt, handler):
    #                 continue
    #             try:
    #                 await handler.handle(evt)
    #             except Exception as e:
    #                 if group_id := getattr(evt, "group_id", None):
    #                     from cqhttp.api.message.SendGroupMsg import SendGroupMsg

    #                     await SendGroupMsg(group_id, "牙白，发生了不知名的错误！").do()
    #                 log.error("error occurred when handling evt:%s", e)
    #                 print(datetime.datetime.now, e)
    #                 raise Exception(handler, evt, e)
    #         if evt._.canceled:
    #             return

    @CQHTTPAdapter.Adapter.websocket("/event")
    async def loop(self):
        while self.bot.is_running:
            evt = await self.rev()
            _t = asyncio.create_task(self.process_evt(evt))
        await self.bot.stop()

    async def rev(self) -> CQHTTPEvent:
        return await self.bot._cqhttp.rev_evt()

    async def post_api(self, act: ApiAction):
        await self.process_evt(act)
        if act._.canceled:
            return
        await self.bot._cqhttp.api(act)
        act._callback()

    @staticmethod
    def is_interested(evt: Event, handler: EventHandler):
        return any(True if isinstance(evt, i) else False for i in handler.interested)


class Bot:
    # public
    services: list[Service] = []
    handlers: dict[Type[Event], list[EventHandler]] = defaultdict(list)

    # private
    _behavior = BotBehavior()
    _db = DataBase()
    _cqhttp = CQHTTPAdapter()

    def __init__(self, name: str, qq_number: int):
        self.name = name
        self.qq_number = qq_number
        self._behavior.set_bot(self)
        self._db.set_bot(self)
        self.is_running = False

    def run(self, endpoint: str):
        host, port = endpoint.split(":")
        self._cqhttp.run(host, int(port))

    async def start_up(self):
        if self.is_running:
            log.warning("already start up!")
            return

        # init database
        if not os.path.exists("src/db"):
            os.makedirs("src/db")
        db = self._db
        await db.connect("src/db/%s.db" % self.name)
        db.execute(
            "create table if not exists services (service text primary key,service_on bool)"
        )

        # init services
        from services.base import Service

        services = self.services
        sort_services(services)
        from services.core.base import core_services

        sort_services(core_services)
        services = core_services + services
        services.sort(key=lambda x: x.priority)
        self.services = [s(self) if not isinstance(s, Service) else s for s in services]

        for s in self.services:
            db.execute(
                "select ifnull((select service_on from services where service = ?),true)",
                (s.__class__.__name__,),
            )
            state = db.fatchone()
            if state[0]:
                await s.start_up()

        # init handlers
        from cqhttp.events.base import all_events

        for evt in all_events:
            for s in self.services:
                for h in s.behavior:
                    if not isinstance(h, EventHandler):
                        return
                    if any(issubclass(evt, e) for e in h.interested):
                        self.handlers[evt].append(h)

        # init src
        if not os.path.exists("src/temp"):
            os.makedirs("src/temp")

        self.is_running = True
        print("%s start up!" % self.name)

    async def stop(self):
        if not self.is_running:
            log.warning("already closed")
            return

        await self._cqhttp.shutdown()
        await self._db.close()
        self.is_running = False
        print("%s closed!" % self.name)
