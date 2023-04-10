# -- stdlib --
import logging
from typing import Type, cast
from re import compile, RegexFlag

# -- third party --
# -- own --
from config import Bots
from cqhttp.events.base import CQHTTPEvent
from cqhttp.events.message import GroupMessage, Message, PrivateMessage

# -- code --

log = logging.getLogger("bot.service")


class ServiceCore:
    def __init__(self, bot):
        from bot import Bot

        self.bot = bot = cast(Bot, bot)


class EventHandler(ServiceCore):
    interested: list[Type[CQHTTPEvent]]

    @staticmethod
    async def before_handle(evt: CQHTTPEvent):
        ...

    async def handle(self, evt: CQHTTPEvent):
        ...  # to override it

    @staticmethod
    async def after_handle(evt: CQHTTPEvent):
        ...


class MessageHandler(EventHandler):
    interested: list[Type[Message]]
    entrys = []
    entry_flags = 0

    def __init__(self, service):
        super().__init__(service)
        entry = self.entrys
        self.entrys = [compile(et, self.entry_flags) for et in entry]

    def fliter(self, evt: Message):
        msg = evt.message
        for _entry in self.entrys:
            if match := _entry.match(msg):
                r = match.groupdict()
                return match.groupdict()


class Service:
    service_on = False
    cores = []

    def __init__(self, bot):
        self.cores = [core(bot) for core in self.cores]

    async def start(self):
        self.service_on = True

    async def close(self):
        self.service_on = False


def register_to(*bots):
    if "all" or "ALL" in bots:
        bots = [b.name for b in Bots]

    def register(cls: Type[Service]):
        for b in Bots:
            if b.name in bots:
                b.services.append(cls)
        return cls

    def except_for(*_bots):
        include = [b for b in bots if b not in _bots]
        return register_to(include)

    register.except_for = except_for
    return register
