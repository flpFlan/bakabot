# -- stdlib --
import asyncio
import time

# -- third party --
# -- own --
from services.base import register_service_to, Service, EventHandler
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
            if not (r := evt.response):
                return
            if not (e := getattr(r, "echo", None)):
                return
            if e == "msg_failed_echo":
                return
            time.sleep(1)
            if not r.status == "failed":
                return
            assert evt.group_id
            asyncio.create_task(
                SendGroupMsg(evt.group_id, "谔谔，该消息被腾讯拦截", echo="msg_failed_echo").do()
            )

        evt._callback = echo


@register_service_to("ALL")
class MessageFailedEcho(Service):
    cores = [MessageFailedEchoCore]
