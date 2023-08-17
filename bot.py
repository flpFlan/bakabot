# -- stdlib --
import asyncio
import logging, os
from typing import TYPE_CHECKING, Literal, Optional, TypeVar, overload
from inspect import isabstract

# -- own --
from adapter import CQHTTPAdapter

# -- code --
if TYPE_CHECKING:
    from services.base import Service
    from cqhttp.api.base import ApiAction, ResponseBase
    from cqhttp.events.base import CQHTTPEvent

    _TResponse = TypeVar("_TResponse", bound=ResponseBase)

log = logging.getLogger("bot")


class BotBehavior:
    def __init__(self, bot: "Bot"):
        self.bot = bot

    async def process_cqhttp_evt(self, evt: "CQHTTPEvent"):
        for service in self.bot.services:
            await service.handle(evt)

    @overload
    async def process_api_action(self, act: "ApiAction", is_before_post: Literal[True]):
        ...

    @overload
    async def process_api_action(
        self, act: "ApiAction", is_before_post: Literal[False], arg: "ResponseBase"
    ):
        ...

    async def process_api_action(
        self,
        act: "ApiAction",
        is_before_post: bool,
        arg: Optional["ResponseBase"] = None,
    ):
        p = (act, True, None) if is_before_post else (act, False, arg)
        for service in self.bot.services:
            await service.handle(p) # type: ignore

    async def evt_loop(self):
        while True:
            evt = await self.rev()
            _t = asyncio.create_task(self.process_cqhttp_evt(evt))

    async def rev(self) -> "CQHTTPEvent":
        return await self.bot.cqhttp.rev_evt()

    async def post_api(self, act: "ApiAction[_TResponse]") -> "_TResponse":
        await self.process_api_action(act, is_before_post=True)
        r = await self.bot.cqhttp.api(act)
        await self.process_api_action(act, is_before_post=False, arg=r)
        return r


class Bot:
    def __init__(self, name: str, qq_number: int):
        self.name = name
        self.qq_number = qq_number
        self.is_running = False
        self.services: list["Service"] = []

    async def run_forever(self):
        while True:
            await self.cqhttp.run()
            log.error("adapter exceptionly shutdown")
            await asyncio.sleep(1)

    async def setup(self):
        log.info("%s loading..." % self.name)

        self.behavior = BotBehavior(self)
        self.cqhttp = CQHTTPAdapter()

        # init database
        if not os.path.exists("src/db"):
            os.makedirs("src/db")
        from accio import ACCIO

        db = ACCIO.db
        await db.connect("src/db/%s.db" % self.name)
        await db.execute(
            "create table if not exists services (service text primary key,service_on bool)"
        )

        # init services
        from services.base import Service

        # NOTE: don't use asyncio.gather, to delay __setup
        g = [await s.create_instance() for s in Service.get_classes() if not isabstract(s)]
        self.services.extend(g)

        for s in self.services:
            await db.execute(
                "select ifnull((select service_on from services where service = ?),true)",
                (s.__class__.__name__,),
            )
            state = await db.fatchone()
            if state and state[0]:
                await s.start()

        # init src
        if not os.path.exists("src/temp"):
            os.makedirs("src/temp")

        # other
        self.SUPERUSER = ACCIO.conf.getint("Bot", "superuser")
        self.Administrators: list[int] = eval(ACCIO.conf.get("Bot", "administrators"))

        self.is_running = True
        log.info("%s start up!" % self.name)

    async def stop(self):
        raise Exception("can't stop")
        # if not self.is_running:
        #     log.warning("already closed")
        #     return

        # await self._cqhttp.shutdown()
        # from accio import ACCIO

        # await ACCIO.db.close()
        # self.is_running = False
        # log.info("%s closed!" % self.name)
