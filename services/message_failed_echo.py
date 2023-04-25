# -- stdlib --
import asyncio

# -- third party --
# -- own --
from services.base import register_to, Service, EventHandler
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from cqhttp.api.message.SendMsg import SendMsg

# -- code --


class MessageFailedEchoCore(EventHandler):
    interested = [SendGroupMsg, SendMsg]

    async def handle(self, evt: SendGroupMsg | SendMsg):
        if isinstance(evt, SendMsg):
            if not getattr(evt, "group_id", None):
                return

        def echo():
            if evt.response.status == "failed":
                assert evt.group_id
                asyncio.ensure_future(
                    SendGroupMsg(evt.group_id, "谔谔，该消息被腾讯拦截").do(self.bot)
                )

        evt._callback = echo


@register_to("ALL")
class MessageFailedEcho(Service):
    cores = [MessageFailedEchoCore]
