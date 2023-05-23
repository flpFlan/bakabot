# -- stdlib --
# -- third party --
import random
from typing import cast

# -- own --
from services.base import register_service_to, Service, EventHandler
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.request import Request

# -- code --
url = "https://raw.githubusercontent.com/Nthily/KFC-Crazy-Thursday/main/kfc.json"
url2 = "https://gitee.com/Nicr0n/fucking_crazy_thursday/raw/master/post.json"


class KFCCore(EventHandler):
    interested = [GroupMessage]

    async def handle(self, evt: GroupMessage):
        if not evt.message == "疯狂星期四文案生成":
            return
        service = cast(KFC, self.service)
        m = random.choice(service.texts)

        await SendGroupMsg(evt.group_id, m).do()


@register_service_to("ALL")
class KFC(Service):
    cores = [KFCCore]

    async def start_up(self):
        await super().start_up()
        self.texts = await self.get_texts()

    async def get_texts(self):
        r = Request.Sync.get_json(url)
        texts = [t["text"] for t in r]
        r = Request.Sync.get_json(url2)
        texts.extend(r["post"])
        return texts
