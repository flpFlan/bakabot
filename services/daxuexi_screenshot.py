# -- stdlib --
import requests

# -- third party --
# -- own --
from services.base import Service, ServiceBehavior, OnEvent
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.request import Request
from cqhttp.cqcode import Image

# -- code --


class DaXueXiScreenshot(Service):
    name = "青年大学习截图生成"


class ScreenshotCore(ServiceBehavior[DaXueXiScreenshot]):
    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if not evt.message == "青年大学习截图生成":
            return
        try:
            url = await self.get_screenshot()
            m = f"{Image(file=url)}"
        except requests.ConnectTimeout:
            m = "请求超时(Ｔ▽Ｔ)"

        SendGroupMsg(evt.group_id, m).forget()

    async def get_screenshot(self):
        req_url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/common-api/course/current"
        response = await Request[dict].get_json(req_url)
        url = response["result"]["uri"]
        if url.find("index.html") != -1:
            url = url.replace("index.html", "images/end.jpg")
        elif url.find("m.html") != -1:
            url = response["result"]["uri"][:-6] + "images/end.jpg"
        return url
