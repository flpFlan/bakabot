# -- stdlib --
import re

# -- third party --
# -- own --
from services.base import Service, ServiceBehavior, OnEvent, IMessageFilter
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from .bilibili_cover import av_to_bv, bv_to_av

# -- code --


class BilibiliABTrans(Service):
    pass


class BilibiliABTransCore(ServiceBehavior[BilibiliABTrans], IMessageFilter):
    entrys = [
        r"^(?P<type>av)号转换\s*(av)?(?P<arg>\d+)",
        r"^(?P<type>bv)号转换\s*(bv)?(?P<arg>\w+)",
    ]
    entry_flags = re.I

    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if r := self.filter(evt):
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
