# -- stdlib --
import asyncio, logging, os, json
from typing import TYPE_CHECKING, Literal, Optional, TypeVar, overload
from inspect import isabstract

# -- own --
from adapter import CQHTTPAdapter
from accio import ACCIO

# -- third party --

# -- code --
if TYPE_CHECKING:
    from services.base import Service
    from cqhttp.api.base import ApiAction, ResponseBase
    from cqhttp.events.base import CQHTTPEvent

    _TResponse = TypeVar("_TResponse", bound=ResponseBase)

log = logging.getLogger("bot")


class BotBehavior:
    async def process_cqhttp_evt(self, evt: "CQHTTPEvent"):
        for service in ACCIO.bot.services:
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
        for service in ACCIO.bot.services:
            await service.handle(p)  # type: ignore

    async def evt_loop(self):
        while True:
            evt = await self.rev()
            _t = asyncio.create_task(self.process_cqhttp_evt(evt))

    async def rev(self) -> "CQHTTPEvent":
        return await ACCIO.bot.cqhttp.rev_evt()

    async def post_api(self, act: "ApiAction[_TResponse]") -> "_TResponse":
        await self.process_api_action(act, is_before_post=True)
        r = await ACCIO.bot.cqhttp.api(act)
        await self.process_api_action(act, is_before_post=False, arg=r)
        return r


class Bot:
    def __init__(self, name: str, qq_number: int):
        self.name = name
        self.qq_number = qq_number
        self.is_running = False
        self.services: list["Service"] = []
        self.SUPERUSER = ACCIO.conf.getint("Bot", "superuser")
        self.Administrators: list[int] = json.loads(ACCIO.conf.get("Bot", "administrators"))
        self.behavior = BotBehavior()
        self.cqhttp = CQHTTPAdapter()

    async def run_forever(self):
        self.is_running = True
        await self.cqhttp.run()
        log.error("adapter exceptionly shutdown")
        await self.stop()

    async def install_services(self):
        log.info("install service...")

        from services.base import Service
        from db.models import Service as ServiceModel

        # NOTE: don't use asyncio.gather, to delay __setup
        g = [
            await s.create_instance()
            for s in Service.get_classes()
            if not isabstract(s)
        ]
        self.services.extend(g)
        session = ACCIO.db.session
        async with session.begin():
            for service in self.services:
                rslt = await session.get(ServiceModel, service.__class__.__name__)
                if not rslt:
                    rslt = ServiceModel(name=service.__class__.__name__)
                    session.add(rslt)
                if rslt.service_on:
                    await service.start()
            await session.commit()
        
        log.info("all services were installed")

    async def stop(self):
        raise Exception("can't stop")
