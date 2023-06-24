# -- stdlib --
import os

# -- third party --

# -- own --
from services.base import Service, ServiceBehavior, OnEvent
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.request import Request
from cqhttp.cqcode import Image

# -- code --


class NowdayNews(Service):
    pass


class NowdayNewsCore(ServiceBehavior[NowdayNews]):
    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if not evt.message == "读懂世界":
            return
        await self.get_everyday_news()
        path = os.path.abspath(r".\src\temp\nowday_news_temp.png")
        await SendGroupMsg(evt.group_id, Image(f"file:///{path}")).do()

    async def get_everyday_news(self):
        url = "http://bjb.yunwj.top/php/tp/1.jpg"
        with open(r".\src\temp\nowday_news_temp.png", "wb") as file:
            for i in Request.Sync.get_iter_content(url):
                file.write(i)
            file.close()
