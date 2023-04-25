# -- stdlib --
import json
import os
import random
import requests

# -- third party --

# -- own --
from services.base import register_to, Service, IMessageFilter, EventHandler
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.request import Request

# -- code --


class SearchImageCore(EventHandler, IMessageFilter):
    interested = [GroupMessage]
    entrys = [r"^搜图\s*(?P<tag>.*)"]

    async def handle(self, evt: GroupMessage):
        if r := self.filter(evt):
            tag = r.get("tag", "")
            if not tag or tag.isspace():
                m = "(?˙▽˙?)请告诉妾身搜索内容哦"
            else:
                try:
                    self.search(tag)
                    path = os.path.abspath(r".\src\temp\search_img_temp.jpg")
                    m = f"[CQ:image,file=file:///{path}]"
                except requests.ConnectTimeout:
                    m = "请求超时(Ｔ▽Ｔ)"
            await SendGroupMsg(evt.group_id, m).do(self.bot)

    def search(self, tag):
        url = f"https://image.baidu.com/search/acjson?tn=resultjson_com&word={tag}&pn=0"
        response = Request.get(url, timeout=10).text
        response = json.loads(response)
        url = response["data"][random.randint(0, 29)]["thumbURL"]
        response = Request.get(url)
        response.raise_for_status()
        with open(r".\src\temp\search_img_temp.jpg", "wb") as file:
            for i in response.iter_content(100000):
                file.write(i)


@register_to("ALL")
class SearchImage(Service):
    cores = [SearchImageCore]
