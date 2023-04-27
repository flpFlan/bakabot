# -- stdlib --
import asyncio
import logging, os
import datetime
from typing import cast

# -- third party --

# -- own --
from adapter import CQHTTPAdapter
from cqhttp.base import Event
from cqhttp.api.base import ApiAction
from cqhttp.events.base import CQHTTPEvent
from db.database import DataBase


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
    def __init__(self, bot):
        self.bot = bot = cast(Bot, bot)

    async def process_evt(self, evt: Event):
        bot = self.bot
        for service in bot.services:
            if not service.service_on:
                continue
            from services.base import EventHandler

            for handler in service.cores:
                if not handler.core_on:
                    continue
                if not isinstance(handler, EventHandler):
                    continue
                if not any(
                    [True if isinstance(evt, i) else False for i in handler.interested]
                ):
                    continue
                try:
                    await handler.handle(evt)
                except Exception as e:
                    if group_id := getattr(evt, "group_id", None):
                        from cqhttp.api.message.SendGroupMsg import SendGroupMsg

                        await SendGroupMsg(group_id, "牙白，发生了不知名的错误！").do(bot)
                    log.error("error occurred when handling evt:%s", e)
                    print(datetime.datetime.now, e)
                    raise Exception(handler, evt, e)
            if evt._.canceled:
                return

    async def loop(self, loop):
        if self.bot.is_running:
            evt = await self.rev()
            loop.create_task(self.process_evt(evt))
        # loop.call_soon_threadsafe(asyncio.create_task, self.loop(loop))
        loop.call_soon(asyncio.create_task, self.loop(loop))

    async def rev(self) -> CQHTTPEvent:
        bot = self.bot
        return await bot.go.rev_evt()

    async def post_api(self, act: ApiAction):
        await self.process_evt(act)
        if act._.canceled:
            return
        await self.bot.go.api(act)
        act._callback()


class Bot:
    is_running = False
    services = []

    def __init__(self, name: str, qq_number: int):
        self.name = name
        self.qq_number = qq_number
        self.behavior = BotBehavior(self)
        self.go = CQHTTPAdapter(self)
        self.db = DataBase(self)

    async def start_up(self, endpoint):
        if self.is_running:
            log.warning("already start up!")
            return

        # init backend
        go = self.go
        await go.connect("ws://" + endpoint)

        # init database
        if not os.path.exists("src/db"):
            os.makedirs("src/db")
        db = self.db
        name = self.name
        await db.connect("src/db/%s.db" % name)
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
                await s.start()

        # init src
        if not os.path.exists("src/temp"):
            os.makedirs("src/temp")

        self.is_running = True
        print("%s start up!" % name)

    async def stop(self):
        if not self.is_running:
            log.warning("already closed")
            return

        await self.go.disconnect()
        await self.db.close()
        self.is_running = False
        print("%s closed!" % self.name)
