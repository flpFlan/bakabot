# -- stdlib --
import asyncio
import logging, os
import time
from typing import TYPE_CHECKING, Literal, Optional, TypeVar, overload

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
        [service.feed(evt) for service in self.bot.services]

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
        if is_before_post:
            p = (act, True, None)
        else:
            assert arg
            p = (act, False, arg)
        t = [asyncio.create_task(service.handle(p)) for service in self.bot.services]
        await asyncio.wait(t)

    async def evt_loop(self):
        while True:
            evt = await self.rev()
            from cqhttp.events.message import Message

            if isinstance(evt, Message):
                if evt.message==".r":
                    print(time.time())
            await self.process_cqhttp_evt(evt)

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

    async def run(self, host: str, port: int):
        await self.cqhttp.run(host, int(port))

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
        db.execute(
            "create table if not exists services (service text primary key,service_on bool)"
        )

        # init services
        from services.base import Service

        # NOTE: don't use asyncio.gather, to delay __setup
        g = [await s.create_instance() for s in Service.get_classes()]
        self.services.extend(g)

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
