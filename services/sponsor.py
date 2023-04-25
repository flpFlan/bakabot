# -- stdlib --
import os
import requests

# -- third party --
# -- own --
from services.base import IMessageFilter, register_to, Service, EventHandler
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg

# -- code --


class SponsorCore(EventHandler):
    interested = [GroupMessage]

    async def handle(self, evt: GroupMessage):
        if not evt.message == "赞助":
            return
        webchat = os.path.abspath(r"src\sponsor\webchat.png")
        alipay = os.path.abspath(r"src\sponsor\alipay.jpg")
        m = f"""
Buy me a coffee :)

>>>微信
[CQ:image,file=file:///{webchat}]

>>>支付宝
[CQ:image,file=file:///{alipay}]
""".strip()

        await SendGroupMsg(evt.group_id, m).do(self.bot)


@register_to("BAKA")
class Sponsor(Service):
    cores = [SponsorCore]
