# -- stdlib --
import asyncio
import time

# -- third party --
# -- own --
from services.base import Service, ServiceBehavior, OnEvent
from cqhttp.api.message.SendGroupMsg import SendGroupMsg, Response as R2
from cqhttp.api.message.SendMsg import SendMsg, Response as R1

# -- code --


class MessageFailedEcho(Service):
    pass


class MessageFailedEchoCore(ServiceBehavior[MessageFailedEcho]):
    @OnEvent[SendGroupMsg, SendMsg].AfterPost.add_listener
    async def handle(self, evt: SendGroupMsg | SendMsg, args: R1 | R2):
        if isinstance(evt, SendMsg):
            if not getattr(evt, "group_id", None):
                return
        if not args["status"] == "failed":
            return
        if args.get("echo", None) == "msg_failed_echo":
            return
        assert evt.group_id
        SendGroupMsg(evt.group_id, "谔谔，该消息被腾讯拦截", echo="msg_failed_echo").forget()
