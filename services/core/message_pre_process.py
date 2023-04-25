# -- stdlib --

# -- third party --
# -- own --
from services.core.base import core_service
from services.base import EventHandler, Service
from cqhttp.events.message import Message


# -- code --
class Process(EventHandler):
    interested = [Message]

    async def handle(self, evt: Message):
        msg = evt.message
        msg = msg.replace("&amp;", "&")
        msg = msg.replace("&#91;", "[")
        msg = msg.replace("&#93;", "]")
        msg = msg.replace("&#44;", ",")
        evt.message = msg


@core_service
class MessagePreProcess(Service):
    priority = -1
    cores = [Process]

    async def close(self):
        pass
