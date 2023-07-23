# -- stdlib --

# -- third party --
# -- own --
from services.base import ServiceBehavior, Service, OnEvent
from cqhttp.events.message import Message


# -- code --


class MessagePreProcess(Service):
    pass


class Process(ServiceBehavior[MessagePreProcess]):
    @OnEvent[Message].add_listener
    async def handle(self, evt: Message):
        # TODO: use subscript
        evt.message = (
            evt.message.replace("&amp;", "&")
            .replace("&#91;", "[")
            .replace("&#93;", "]")
            .replace("&#44;", ",")
        )
