# -- stdlib --
import os
import random
import requests

# -- third party --

# -- own --
from services.base import Service, ServiceBehavior, OnEvent, IMessageFilter
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.request import Request
from cqhttp.cqcode import Image

# -- code --


class SearchImage(Service):
    name = "搜图"
    doc = """出了点问题，以后再修。"""


class SearchImageCore(ServiceBehavior[SearchImage], IMessageFilter):
    entrys = [r"^搜图\s*(?P<tag>.*)"]

    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if not (r := self.filter(evt)):
            return
        tag = r["tag"]
        if not tag or tag.isspace():
            m = "(?˙▽˙?)请告诉妾身搜索内容哦"
        else:
            try:
                await self.search(tag)
                path = os.path.abspath(r".\src\temp\search_img_temp.jpg")
                m = f"{Image(f'file:///{path}')}"
            except requests.ConnectTimeout:
                m = "请求超时(Ｔ▽Ｔ)"
        await SendGroupMsg(evt.group_id, m).do()

    async def search(self, tag):
        url = f"https://image.baidu.com/search/acjson?tn=resultjson_com&word={tag}&pn=0"
        response = await Request[dict].get_json(url, timeout=10)
        url = response["data"][random.randint(0, 29)]["thumbURL"]
        with open(r".\src\temp\search_img_temp.jpg", "wb") as file:
            for i in await Request.get_iter_content(url):
                file.write(i)
            file.close()
