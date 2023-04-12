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
                if not isinstance(handler, EventHandler):
                    continue
                if not any(
                    [True if isinstance(evt, i) else False for i in handler.interested]
                ):
                    continue
                await handler.handle(evt)
            if evt._.canceled:
                return

    async def loop(self):
        while True:
            evt = await self.rev()
            await self.process_evt(evt)

    async def run(self, endpoint: str):
        bot = self.bot
        if bot.is_running:
            log.warning("already running")
            return

        await bot.go.connect("ws://" + endpoint)
        if not os.path.exists("data/db"):
            os.makedirs("data/db")
        await bot.db.connect("data/db/%s.db" % bot.name)

        from services.base import Service

        services = bot.services
        sort_services(services)
        from services.core.base import core_services

        sort_services(core_services)
        services = core_services + services
        bot.services = [s(bot) if not isinstance(s, Service) else s for s in services]
        for s in bot.services:
            await s.start()

        bot.is_running = True
        print("%s started！" % bot.name)
        await self.loop()

        log.warning("%s shootdown :(" % bot.name)
        await self.stop()

    async def stop(self):
        bot = self.bot
        if not bot.is_running:
            log.warning("already closed")
            return

        await bot.go.disconnect()
        await bot.db.close()
        bot.is_running = False
        print("%s closed!" % bot.name)

    async def rev(self) -> CQHTTPEvent:
        bot = self.bot
        return await bot.go.rev_evt()

    async def post_api(self, act: ApiAction):
        bot = self.bot
        act._.before_post = True
        await self.process_evt(act)
        await bot.go.api(act)
        act._.before_post = False
        await self.process_evt(act)


class Bot:
    is_running = False
    services = []

    def __init__(self, name: str, qq_number: int):
        self.name = name
        self.qq_number = qq_number
        self.behavior = BotBehavior(self)
        self.go = CQHTTPAdapter(self)
        self.db = DataBase(self)
