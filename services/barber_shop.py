# -- stdlib --
# -- third party --
import random

# -- own --
from services.base import IMessageFilter, Service, ServiceBehavior, OnEvent
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.request import Request

# -- code --
url = "https://raw.githubusercontent.com/xipesoy/zhenxun_plugin_meiriyiju/main/resource/post.json"


class BarberShop(Service):
    async def __setup(self):
        self.words = await self.get_words()

    async def get_words(self) -> list[str]:
        r = await Request[dict].get_json(url)
        return r["post"]


class BarberShopCore(ServiceBehavior[BarberShop], IMessageFilter):
    entrys = [r"^发电\s*(?P<name>[\S]{1,23})"]

    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if not (r := self.filter(evt)):
            return
        word = random.choice(self.service.words).replace("阿咪", r["name"])

        await SendGroupMsg(evt.group_id, word).do()
