# -- stdlib --
import re

# -- third party --
# -- own --
from services.base import register_service_to, Service, IMessageFilter, EventHandler
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from .bilibili_cover import av_to_bv, bv_to_av

# -- code --


class BilibiliABTransCore(EventHandler, IMessageFilter):
    interested = [GroupMessage]
    entrys = [
        r"^(?P<type>av)号转换\s*(av)?(?P<arg>\d+)",
        r"^(?P<type>bv)号转换\s*(bv)?(?P<arg>\w+)",
    ]
    entry_flags = re.I

    async def handle(self, evt: GroupMessage):
        if r := self.filter(evt):
            bot = self.bot
            group_id = evt.group_id
            type = r.get("type", "").lower()
            arg = r.get("arg", "")
            if type == "av":
                id = self.trans_av(arg)
            else:
                id = self.tans_bv(arg)
            await SendGroupMsg(group_id, str(id)).do()

    def tans_bv(self, arg: str):
        arg = "BV" + arg
        try:
            return bv_to_av(arg)
        except:
            return "转换失败"

    def trans_av(self, arg: str):
        try:
            return av_to_bv(int(arg))
        except:
            return "转换失败"


@register_service_to("ALL")
class BilibiliABTrans(Service):
    cores = [BilibiliABTransCore]
