# -- stdlib --
import re
import requests

# -- third party --
# -- own --
from services.base import register_to, Service, IMessageFilter, EventHandler
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.request import Request

# -- code --

table = "fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF"
tr = {}
for i in range(58):
    tr[table[i]] = i
s = [11, 10, 3, 8, 4, 6]
xor = 177451812
add = 8728348608


def bv_to_av(x: str) -> int:
    r = 0
    for i in range(6):
        r += tr[x[s[i]]] * 58**i
    return (r - add) ^ xor


def av_to_bv(x: int) -> str:
    x = (x ^ xor) + add
    r = list("BV1  4 1 7  ")
    for i in range(6):
        r[s[i]] = table[x // 58**i % 58]
    return "".join(r)


class BilibiliCoverCore(EventHandler, IMessageFilter):
    interested = [GroupMessage]
    entrys = [r"^b站封面获取(?P<type>live|cv|av|bv)?(?P<arg>\w+)"]
    entry_flags = re.I

    async def handle(self, evt: GroupMessage):
        if not (r := self.filter(evt)):
            return
        bot = self.bot
        group_id = evt.group_id
        type = (r.get("type", "") or "live").lower()
        arg = r.get("arg", "")
        if type == "bv":
            arg = bv_to_av("BV" + arg)
            type = "av"
        if url := await self.get_b_cover(arg, type):
            await SendGroupMsg(group_id, f"[CQ:image,file={url}]").do(bot)
            return
        m = "呜，房间为空" if type == "live" else "呜，稿件为空"
        await SendGroupMsg(group_id, m).do(bot)

    async def get_b_cover(self, id, type="av"):
        url = f"https://apiv2.magecorn.com/bilicover/get?"
        "type={type}&id={id}&client=2.5.2"
        r = Request.Sync.get_json(url)
        return r.get("url", None)


@register_to("ALL")
class BilibiliCover(Service):
    cores = [BilibiliCoverCore]
