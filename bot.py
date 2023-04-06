# -- stdlib --
import asyncio, logging, json, re
from typing import cast

# -- third party --

# -- own --
from adapter import CQHTTPAdapter

# -- code --
log = logging.getLogger("Bot")


class BotBehavior:
    def __init__(self, bot):
        self.bot = bot = cast(Bot, bot)

    async def loop(self):
        while True:
            ...


class Bot:
    is_running: bool = False
    services = []

    def __init__(self, name: str, qq_number: int):
        self.name = name
        self.qq_number = qq_number
        self.behavior = BotBehavior(self)
        self.go = CQHTTPAdapter(self)

    async def run(self, evt_adr: str, api_adr: str):
        if self.is_running:
            log.debug("already running")
            return

        await self.go.connect(evt_adr, api_adr)

        for s in self.services:
            # s.entry = s.entry or []
            # s.entry = [re.compile(e, s.entry_flags or 0) for e in s.entry]
            s.start()

        self.is_running = True
        await self.behavior.loop()

        log.debug("bot shootdown")
        await self.close()

    async def close(self):
        if not self.is_running:
            log.debug("already closed")
            return

        await self.go.disconnect()
        self.is_running = False

    async def rev(self) -> dict:
        return await self.go.rev()

    async def api(self, action: str, echo="", **params) -> dict:
        return await self.go.post_api(action, echo, **params)
