# -- stdlib --

# -- third party --
# -- own --
from .base import CoreService
from services.base import ServiceBehavior, OnEvent
from cqhttp.events.message import Message


# -- code --


class MessagePreProcess(CoreService):
    pass


class Process(ServiceBehavior[MessagePreProcess]):
    @OnEvent[Message].add_listener
    async def handle(self, evt: Message):
        evt.message = (
            evt.message.replace("&amp;", "&")
            .replace("&#91;", "[")
            .replace("&#93;", "]")
            .replace("&#44;", ",")
        )
