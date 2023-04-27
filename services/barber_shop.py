# -- stdlib --
# -- third party --
import random
from typing import cast

# -- own --
from services.base import IMessageFilter, register_to, Service, EventHandler
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.request import Request

# -- code --
url = "https://raw.githubusercontent.com/xipesoy/zhenxun_plugin_meiriyiju/main/resource/post.json"


class BarberShopCore(EventHandler, IMessageFilter):
    interested = [GroupMessage]
    entrys = [r"^发电(?P<name>[\S]{1,23})"]

    async def handle(self, evt: GroupMessage):
        if not (r := self.filter(evt)):
            return
        name = r.get("name", "noname")
        service = cast(BarberShop, self.service)
        word = random.choice(service.words).replace("阿咪", name)

        await SendGroupMsg(evt.group_id, word).do(self.bot)


@register_to("ALL")
class BarberShop(Service):
    cores = [BarberShopCore]

    async def start(self):
        await super().start()
        self.words = await self.get_words()

    async def get_words(self) -> list[str]:
        r = Request.Sync.get_json(url)
        return r["post"]
