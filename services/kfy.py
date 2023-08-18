# -- stdlib --
# -- third party --
import random

# -- own --
from services.base import Service, ServiceBehavior, OnEvent
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.request import Request

# -- code --
url = "https://raw.githubusercontent.com/Nthily/KFC-Crazy-Thursday/main/kfc.json"
url2 = "https://gitee.com/Nicr0n/fucking_crazy_thursday/raw/master/post.json"

doc = """
用例:
    疯狂星期四文案生成
""".strip()


class KFC(Service):
    doc = doc

    async def __setup(self):
        self.texts = await self.get_texts()

    async def get_texts(self):
        r = await Request[dict].get_json(url)
        texts = [t["text"] for t in r]
        r = await Request[dict].get_json(url2)
        texts.extend(r["post"])
        return texts


class KFCCore(ServiceBehavior[KFC]):
    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if not evt.message == "疯狂星期四文案生成":
            return
        m = random.choice(self.service.texts)

        SendGroupMsg(evt.group_id, m).forget()
