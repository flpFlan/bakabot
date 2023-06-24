# -- stdlib --
import asyncio
import logging, os
from typing import TYPE_CHECKING, Optional, cast
from accio import ACCIO

# -- third party --

# -- own --
from adapter import CQHTTPAdapter
from cqhttp.api.base import ApiAction
from cqhttp.events.base import CQHTTPEvent
from services.base import Service


# -- code --
if TYPE_CHECKING:
    from services.base import Service

log = logging.getLogger("bot")


# def sort_services(services):
#     graph = {}
#     for seivice in services:
#         graph[seivice] = {
#             "before": set(seivice.execute_before),
#             "after": set(seivice.execute_after),
#         }
#         for dep in seivice.execute_before:
#             graph[dep]["after"].add(seivice)
#         for dep_by in seivice.execute_after:
#             graph[dep_by]["before"].add(seivice)

#     queue = [service for service, dep in graph.items() if not dep["before"]]
#     result = []
#     while queue:
#         service = queue.pop(0)
#         result.append(service)
#         for dep_by in graph[service]["after"]:
#             graph[dep_by]["before"].remove(service)
#             if not graph[dep_by]["before"]:
#                 queue.append(dep_by)

#     for i, service in enumerate(result):
#         for dep in service.execute_before:
#             dep_idx = services.index(dep())
#             if dep_idx >= i:
#                 services[i], services[dep_idx] = services[dep_idx], services[i]
#                 i = dep_idx
#         for dep_by in service.execute_after:
#             dep_by_index = services.index(dep_by())
#             if dep_by_index <= i:
#                 services[dep_by_index], services[i] = (
#                     services[i],
#                     services[dep_by_index],
#                 )


class BotBehavior:
    def set_bot(self, bot):
        self.bot = cast(Bot, bot)

    async def process_cqhttp_evt(self, evt: CQHTTPEvent):
        _t = asyncio.gather(service.feed(evt) for service in self.bot.services)

    async def process_api_action(
        self, act: ApiAction, is_before_post: bool, arg: Optional[dict] = None
    ):
        _t = asyncio.gather(
            service.feed((act, is_before_post, arg)) for service in self.bot.services
        )

    @CQHTTPAdapter.Adapter.websocket("/event")
    async def evt_loop(self):
        while True:
            evt = await self.rev()
            _t = asyncio.create_task(self.process_cqhttp_evt(evt))

    async def rev(self) -> CQHTTPEvent:
        return await self.bot._cqhttp.rev_evt()

    async def post_api(self, act: ApiAction):
        await self.process_api_action(act, is_before_post=False)
        r = await self.bot._cqhttp.api(act)
        await self.process_api_action(act, is_before_post=True, arg=r)
        return r


class Bot:
    # private
    _behavior = BotBehavior()
    _cqhttp = CQHTTPAdapter()

    def __init__(self, name: str, qq_number: int):
        self._behavior.set_bot(self)
        self.name = name
        self.qq_number = qq_number
        self.is_running = False
        self.services: list[Service] = []

    def run(self, host: str, port: int):
        self._cqhttp.run_at(host, int(port))

    async def set_up(self):
        log.info("%s loading..." % self.name)

        # init database
        if not os.path.exists("src/db"):
            os.makedirs("src/db")
        from accio import ACCIO

        db = ACCIO.db
        await db.connect("src/db/%s.db" % self.name)
        db.execute(
            "create table if not exists services (service text primary key,service_on bool)"
        )

        # init services
        for s in self.services:
            db.execute(
                "select ifnull((select service_on from services where service = ?),true)",
                (s.__class__.__name__,),
            )
            state = db.fatchone()
            if state[0]:
                await s.start_up()

        # init src
        if not os.path.exists("src/temp"):
            os.makedirs("src/temp")

        self.is_running = True
        log.info("%s start up!" % self.name)

    async def stop(self):
        if not self.is_running:
            log.warning("already closed")
            return

        await self._cqhttp.shutdown()
        await ACCIO.db.close()
        self.is_running = False
        log.info("%s closed!" % self.name)
