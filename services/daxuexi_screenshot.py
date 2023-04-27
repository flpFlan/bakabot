# -- stdlib --
import requests

# -- third party --
# -- own --
from services.base import register_to, Service, EventHandler
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.request import Request

# -- code --


class ScreenshotCore(EventHandler):
    interested = [GroupMessage]

    async def handle(self, evt: GroupMessage):
        if not evt.message == "青年大学习截图生成":
            return
        try:
            url = await self.get_screenshot()
            m = f"[CQ:image,file={url}]"
        except requests.ConnectTimeout:
            m = "请求超时(Ｔ▽Ｔ)"

        await SendGroupMsg(evt.group_id, m).do(self.bot)

    async def get_screenshot(self):
        req_url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/common-api/course/current"
        response = Request.Sync.get_json(req_url)
        url = response["result"]["uri"]
        if url.find("index.html") != -1:
            url = url.replace("index.html", "images/end.jpg")
        elif url.find("m.html") != -1:
            url = response["result"]["uri"][:-6] + "images/end.jpg"
        return url


@register_to("ALL")
class DaXueXiScreenshot(Service):
    cores = [ScreenshotCore]
