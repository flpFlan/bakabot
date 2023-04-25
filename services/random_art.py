# -- stdlib --
import json
import random
import requests
from urllib.request import urlopen

# -- third party --

# -- own --
from services.base import register_to, Service, IMessageFilter, EventHandler
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.request import Request

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


class RandomArtCore(EventHandler, IMessageFilter):
    interested = [GroupMessage]
    entrys = [r"^随机图片\s*(?P<tag>.+)?"]

    async def handle(self, evt: GroupMessage):
        if r := self.filter(evt):
            try:
                if tag := r.get("tag", ""):
                    if url := self.search_random(tag):
                        m = f"[CQ:image,file={url}]"
                    else:
                        m = "没有找到相关图片Σ( ° △ °|||)"
                else:
                    url = self.get_random()
                    m = f"[CQ:image,file={url}]"
            except requests.ConnectTimeout:
                m = "请求超时(Ｔ▽Ｔ)"
            await SendGroupMsg(evt.group_id, m).do(self.bot)

    def get_random(self):
        type = random.getrandbits(1)
        if type == 0:
            key = ["img", "imgurl"]
            global urllist

            url = random.choice(urllist_0)

            resonse = Request.get(url, timeout=10).json()
            for i in key:
                if i in resonse:
                    if resonse[i].startswith("//"):
                        resonse[i] = "http:" + resonse[i]
                    return resonse[i]
        else:
            url = random.choice(urllist_1)
            return urlopen(url, timeout=5).geturl()

    def search_random(self, tag):
        for c in reversed(range(6)):
            data = {"str": tag, "id": 24 * random.randint(0, c)}
            res = Request.get(
                f'https://www.duitang.com/napi/blogv2/list/by_search/?kw={data["str"]}&after_id={data["id"]}',
                timeout=10,
            ).text
            if len(res) >= 50:
                break
        assert res  # type: ignore
        if res.startswith("\ufeff"):
            res = res.encode("utf-8")[3:].decode("utf-8")
        res = json.loads(res)
        if data := res.get("data", None):
            if all_arts := data.get("object_list", None):
                i = random.choice(all_arts)
                return i["photo"]["path"].replace(".gif_jpeg", ".gif")
            return None
        return None


@register_to("ALL")
class RandomArt(Service):
    cores = [RandomArtCore]
