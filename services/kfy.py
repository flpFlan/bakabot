# -- stdlib --
# -- third party --
import random
from typing import cast

# -- own --
from services.base import register_to, Service, EventHandler
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.request import Request

# -- code --
url = "https://github.com/whitescent/KFC-Crazy-Thursday/blob/main/kfc.json"


class KFCCore(EventHandler):
    interested = [GroupMessage]

    async def handle(self, evt: GroupMessage):
        if not evt.message == "疯狂星期四文案生成":
            return
        service = cast(KFC,self.service)
        m=random.choice(service.texts)

        await SendGroupMsg(evt.group_id,m).do(self.bot)


@register_to("ALL")
class KFC(Service):
    cores = [KFCCore]

    async def start(self):
        await super().start()
        self.texts = self.get_texts()

    def get_texts(self):
        r = Request.get(url).json()

        return [t["text"] for t in r]
