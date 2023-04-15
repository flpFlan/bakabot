# -- stdlib --
import logging
from typing import Type, cast
from re import compile

# -- third party --
# -- own --
from config import Bots

# -- code --

log = logging.getLogger("bot.service")


class ServiceCore:
    def __init__(self, service):
        from bot import Bot

        self.service = service = cast(Service, service)
        self.bot = getattr(self, "bot", None) or cast(Bot, None)


class EventHandler(ServiceCore):
    from cqhttp.base import Event

    interested: list[Type[Event]]

    async def handle(self, evt: Event):
        ...  # to override it


class MessageHandler(EventHandler):
    from cqhttp.events.message import Message

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
    execute_before = []
    execute_after = []

    def __init__(self, bot):
        self.bot = bot
        self.cores = [core(self) for core in self.cores]
        for core in self.cores:
            core.bot = bot

    async def start(self):
        bot = self.bot
        db = bot.db
        table = bot.name + "_service"
        service = self.__class__.__name__
        db.execute(
            "insert into %s (service,service_on) values (?,?)" % table, (service, True)
        )
        db.commit()
        self.service_on = True

    async def close(self):
        bot = self.bot
        db = bot.db
        table = bot.name + "_service"
        service = self.__class__.__name__

        db.execute(
            "insert into %s (service,service_on) values (?,?)" % table, (service, False)
        )
        db.commit()
        self.service_on = False


def register_to(*bots):
    if "all" or "ALL" in bots:
        bots = [b.name for b in Bots]

    def register(cls):
        for b in Bots:
            if b.name in bots:
                b.services.append(cls)
        return cls

    def except_for(*_bots):
        include = [b for b in bots if b not in _bots]
        return register_to(include)

    register.except_for = except_for
    return register
