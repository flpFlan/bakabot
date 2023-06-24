# -- stdlib --
from ast import Pass
import json
import random
import requests
from urllib.request import urlopen

# -- third party --

# -- own --
from services.base import OnEvent, Service, ServiceBehavior, IMessageFilter
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.request import Request
from cqhttp.cqcode import Image

# -- code --
urllist_0 = [
    "http://img.xjh.me/random_img.php?type=bg&ctype=nature&return=json",
    "http://img.xjh.me/random_img.php?type=bg&ctype=acg&return=json",
    "https://www.dmoe.cc/random.php?return=json",
]
urllist_1 = [
    "https://api.ghser.com/random/api.php",
    "https://api.ghser.com/random/pe.php",
    "https://api.yimian.xyz/img?R18=true",
]


class RandomArt(Service):
    pass


class RandomArtCore(ServiceBehavior[RandomArt], IMessageFilter):
    entrys = [r"^随机图片\s*(?P<tag>.+)?"]

    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if r := self.filter(evt):
            try:
                if tag := r.get("tag", ""):
                    if url := await self.search_random(tag):
                        m = f"{Image(url)}"
                    else:
                        m = "没有找到相关图片Σ( ° △ °|||)"
                else:
                    url = await self.get_random()
                    m = f"{Image(url)}"
            except requests.ConnectTimeout:
                m = "请求超时(Ｔ▽Ｔ)"
            await SendGroupMsg(evt.group_id, m).do()

    async def get_random(self) -> str:
        type = random.getrandbits(1)
        if type == 0:
            key = ["img", "imgurl"]
            url = random.choice(urllist_0)
            resonse = Request.Sync.get_json(url)
            for i in key:
                if i in resonse:
                    if resonse[i].startswith("//"):
                        resonse[i] = "http:" + resonse[i]
                    return resonse[i]
        else:
            url = random.choice(urllist_1)
            return urlopen(url, timeout=5).geturl()

    async def search_random(self, tag):
        for c in reversed(range(6)):
            data = {"str": tag, "id": 24 * random.randint(0, c)}
            url = f'https://www.duitang.com/napi/blogv2/list/by_search/?kw={data["str"]}&after_id={data["id"]}'
            r = Request.Sync.get_text(url, timeout=10)
            if len(r) >= 50:
                break
        assert r  # type: ignore
        if r.startswith("\ufeff"):
            r = r.encode("utf-8")[3:].decode("utf-8")
        r = json.loads(r)
        if data := r.get("data", None):
            if all_arts := data.get("object_list", None):
                i = random.choice(all_arts)
                return i["photo"]["path"].replace(".gif_jpeg", ".gif")
            return None
        return None
