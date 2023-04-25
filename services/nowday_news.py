# -- stdlib --
import os

# -- third party --

# -- own --
from services.base import register_to, Service, EventHandler
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.request import Request

# -- code --


class NowdayNewsCore(EventHandler):
    interested = [GroupMessage]

    async def handle(self, evt: GroupMessage):
        if not evt.message == "读懂世界":
            return
        self.get_everyday_news()
        path = os.path.abspath(r".\src\temp\nowday_news_temp.png")
        await SendGroupMsg(evt.group_id, f"[CQ:image,file=file:///{path}]").do(self.bot)

    def get_everyday_news(self):
        url = "http://bjb.yunwj.top/php/tp/1.jpg"
        response = Request.get(url, timeout=10)
        response.raise_for_status()
        with open(r".\src\temp\nowday_news_temp.png", "wb") as file:
            for i in response.iter_content(100000):
                file.write(i)
            file.close()


@register_to("ALL")
class NowdayNews(Service):
    cores = [NowdayNewsCore]
