# -- stdlib --
import os
import requests

# -- third party --
# -- own --
from services.base import Service, ServiceBehavior, OnEvent
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from cqhttp.cqcode import Image

# -- code --


class Sponsor(Service):
    pass


class SponsorCore(ServiceBehavior[Sponsor]):
    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if not evt.message == "赞助":
            return
        webchat = os.path.abspath(r"src\sponsor\webchat.png")
        alipay = os.path.abspath(r"src\sponsor\alipay.jpg")
        m = f"""
Buy me a coffee :)

>>>微信
{Image(f'file:///{webchat}')}

>>>支付宝
{Image(f'file:///{alipay}')}
""".strip()

        await SendGroupMsg(evt.group_id, m).do()
