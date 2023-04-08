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
            for s in bot.services:
                if not s.service_on:
                    continue
                from services.base import EventHandler

                for h in s.cores:
                    if not isinstance(h, EventHandler):
                        continue
                    if not any(
                        [True if isinstance(evt, i) else False for i in h.interested]
                    ):
                        continue
                    await h.handle(evt)

    async def run(self, addr: str):
        bot = self.bot
        if bot.is_running:
            log.warning("already running")
            return

        await self.bot.go.connect("ws://" + addr)

        from services.base import Service

        services = bot.services
        bot.services = [s(bot) if not isinstance(s, Service) else s for s in services]
        for s in bot.services:
            await s.start()

        bot.is_running = True
        await self.loop()

        log.warning("bot shootdown")
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
