# -- stdlib --
from json import JSONDecodeError
import requests

# -- third party --
# -- own --
from services.base import register_to, Service, IMessageFilter, EventHandler
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.request import Request

# -- code --


class RandomTouHouCore(EventHandler, IMessageFilter):
    interested = [GroupMessage]
    entrys = [r"^随机东方[图片?]?\s*(?P<tag>[\w\s\-_，,]+)?"]

    async def handle(self, evt: GroupMessage):
        if r := self.filter(evt):
            tag = r.get("tag", "")
            if tag:
                tag = tag.replace("，", ",")
                tag = list(
                    map(lambda x: x.strip().lower().replace(" ", "_"), tag.split(","))
                )
                tag = "&tag=".join(tag)
            try:
                url = self.get_random_th(tag)
                m = rf"[CQ:image,file={url}]"
            except JSONDecodeError:
                m = "tag含有非法字符或未获取到相关图片，请重试！"
            except requests.exceptions.ConnectTimeout:
                m = "请求超时(Ｔ▽Ｔ)"
            await SendGroupMsg(evt.group_id, m).do(self.bot)

    def get_random_th(self, tag: str = ""):
        url = f"https://img.paulzzh.tech/touhou/random?type=json&site=all&size=all&tag={tag}"
        return Request.get(url, timeout=10).json().get("url")


@register_to("All")
class RandomTouHou(Service):
    cores = [RandomTouHouCore]
