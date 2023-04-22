# -- stdlib --
import asyncio
import logging, os
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
                await handler.handle(evt)
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
        task = asyncio.create_task(self.bot.go.api(act))
        task.add_done_callback(act._callback)


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
        if not os.path.exists("data/db"):
            os.makedirs("data/db")
        db = self.db
        name = self.name
        await db.connect("data/db/%s.db" % name)
        db.execute("create table if not exists services (service text,service_on bool)")

        # init services
        from services.base import Service

        services = self.services
        sort_services(services)
        from services.core.base import core_services

        sort_services(core_services)
        services = core_services + services
        self.services = [s(self) if not isinstance(s, Service) else s for s in services]
        db.execute("select service,service_on from services")
        db.commit()
        service_status = db.fatchall()
        service_status = {s[0]: s[1] for s in service_status}
        for s in self.services:
            if not service_status.get(s.__class__.__name__, True):
                continue
            await s.start()

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
