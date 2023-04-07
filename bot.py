# -- stdlib --
import asyncio, logging, json, re
from typing import cast

# -- third party --

# -- own --
from adapter import CQHTTPAdapter
from cqhttp.events.base import CQHTTPEvent

# -- code --
log = logging.getLogger("Bot")


class BotBehavior:
    def __init__(self, bot):
        self.bot = bot = cast(Bot, bot)

    async def loop(self):
        bot = self.bot
        while True:
            evt = await bot.rev()
            for s in bot.services:
                if not s.service_on:
                    continue
                from service.base import EventHandler

                for h in s.cores:
                    if not isinstance(h, EventHandler):
                        continue
                    if not any(
                        [True if isinstance(evt, i) else False for i in h.interested]
                    ):
                        continue
                    await h.handle(evt)


class Bot:
    is_running = False
    services = []

    def __init__(self, name: str, qq_number: int):
        self.name = name
        self.qq_number = qq_number
        self.behavior = BotBehavior(self)
        self.go = CQHTTPAdapter(self)

    async def run(self, addr: str):
        if self.is_running:
            log.debug("already running")
            return

        await self.go.connect("ws://" + addr)

        from service.base import Service

        services = self.services
        self.services = [s(self) if not isinstance(s, Service) else s for s in services]
        for s in self.services:
            await s.start()

        self.is_running = True
        await self.behavior.loop()

        log.debug("bot shootdown")
        await self.stop()

    async def stop(self):
        if not self.is_running:
            log.debug("already closed")
            return

        await self.go.disconnect()
        self.is_running = False

    async def rev(self) -> CQHTTPEvent:
        return await self.go.rev_evt()

    async def post_api(self, action: str, echo="", **params) -> dict:
        return await self.go.api(action, echo, **params)
