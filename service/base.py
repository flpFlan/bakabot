# -- stdlib --
import logging
from typing import Type, cast

# -- third party --
# -- own --
from config import Bots
from cqhttp.events.base import CQHTTPEvent
from cqhttp.events.message import GroupMessage, PrivateMessage

# -- code --

log = logging.getLogger("Service")


class ServiceCore:
    def __init__(self, service):
        self.service = service = cast(Service, service)


class EventHandler(ServiceCore):
    interested: list

    async def handle(self, evt: CQHTTPEvent):
        ...  # to override it


class GroupMessageHandler(EventHandler):
    """因为group message handler很常见，就单独拿出来了"""

    interested = [GroupMessage]


class PrivateMessageHandler(EventHandler):
    """因为private message handler很常见，就单独拿出来了"""

    interested = [PrivateMessage]


class Service:
    service_on = True
    cores = []

    def __init__(self, bot):
        from bot import Bot

        self.bot = bot = cast(Bot, bot)
        self.cores = [core(self) for core in self.cores]

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
