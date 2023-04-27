# -- stdlib --
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
        if not (r := self.filter(evt)):
            return
        tag = r.get("tag", "")
        if not tag or tag.isspace():
            m = "(?˙▽˙?)请告诉妾身搜索内容哦"
        else:
            try:
                await self.search(tag)
                path = os.path.abspath(r".\src\temp\search_img_temp.jpg")
                m = f"[CQ:image,file=file:///{path}]"
            except requests.ConnectTimeout:
                m = "请求超时(Ｔ▽Ｔ)"
        await SendGroupMsg(evt.group_id, m).do(self.bot)

    async def search(self, tag):
        url = f"https://image.baidu.com/search/acjson?tn=resultjson_com&word={tag}&pn=0"
        response = Request.Sync.get_json(url, timeout=10)
        url = response["data"][random.randint(0, 29)]["thumbURL"]
        with open(r".\src\temp\search_img_temp.jpg", "wb") as file:
            for i in Request.Sync.get_iter_content(url):
                file.write(i)
            file.close()


@register_to("ALL")
class SearchImage(Service):
    cores = [SearchImageCore]
