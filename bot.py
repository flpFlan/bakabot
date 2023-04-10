# -- stdlib --
import logging
from typing import TypeVar, cast

# -- third party --

# -- own --
from adapter import CQHTTPAdapter
from cqhttp.api.base import ApiAction
from cqhttp.events.base import CQHTTPEvent
from db.database import DataBase


# -- code --
log = logging.getLogger("bot")


class BotBehavior:
    def __init__(self, bot):
        self.bot = bot = cast(Bot, bot)

    async def loop(self):
        bot = self.bot
        while True:
            evt = await self.rev()
            for service in bot.services:
                if not service.service_on:
                    continue
                from services.base import EventHandler

                for handler in service.cores:
                    if not isinstance(handler, EventHandler):
                        continue
                    if evt._.canceled:
                        break
                    if not any(
                        [
                            True if isinstance(evt, i) else False
                            for i in handler.interested
                        ]
                    ):
                        continue
                    await handler.before_handle(evt)
                    # if not evt._
                    await handler.handle(evt)
                    await handler.after_handle(evt)

    async def run(self, endpoint: str):
        bot = self.bot
        if bot.is_running:
            log.warning("already running")
            return

        await bot.go.connect("ws://" + endpoint)

        from services.base import Service

        services = bot.services
        bot.services = [s(bot) if not isinstance(s, Service) else s for s in services]
        for s in bot.services:
            await s.start()

        bot.is_running = True
        print("%s started!" % bot.name)
        await self.loop()

        log.warning("%s shootdown :(" % bot.name)
        await self.stop()

    async def stop(self):
        bot = self.bot
        if not bot.is_running:
            log.warning("already closed")
            return

        await bot.go.disconnect()
        bot.is_running = False

    async def rev(self) -> CQHTTPEvent:
        bot = self.bot
        return await bot.go.rev_evt()

    async def post_api(self, act: ApiAction):
        bot = self.bot
        return await bot.go.api(act)


class Bot:
    is_running = False
    services = []

    def __init__(self, name: str, qq_number: int):
        self.name = name
        self.qq_number = qq_number
        self.behavior = BotBehavior(self)
        self.go = CQHTTPAdapter(self)
        self.db = DataBase(self)


# def sort_service(services:list):
#     graph = {}
#     for cls in services:
#         cls_name = cls.__name__
#         graph[cls_name] = {'depends_on': set(cls.execute_before), 'depended_by': set(cls.execute_after)}
#         for dep_cls in cls.execute_before:
#             graph[dep_cls.__name__]['depended_by'].add(cls_name)
#         for depended_by_cls in cls.stand_after:
#             graph[depended_by_cls.__name__]['depends_on'].add(cls_name)

#     queue = [cls_name for cls_name, dep_info in graph.items() if not dep_info['depends_on']]
#     result = []
#     while queue:
#         cls_name = queue.pop(0)
#         result.append(cls_name)
#         for depended_by_cls_name in graph[cls_name]['depended_by']:
#             graph[depended_by_cls_name]['depends_on'].remove(cls_name)
#             if not graph[depended_by_cls_name]['depends_on']:
#                 queue.append(depended_by_cls_name)

#     for i, cls_name in enumerate(result):
#         cls = eval(cls_name)

#         for dep_cls in cls.execute_before:
#             dep_idx = services.index(dep_cls())
#             if dep_idx >= i:
#                 services[i], services[dep_idx] = services[dep_idx], services[i]
#                 i = dep_idx

#         for depended_by_cls in cls.execute_after:
#             depended_by_idx = services.index(depended_by_cls())
#             if depended_by_idx <= i:
#                 services[depended_by_idx], services
