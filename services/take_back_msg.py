# -- stdlib --
from re import compile

# -- third party --
# -- own --
from services.base import register_to, Service, EventHandler, IMessageFilter
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.DeleteMsg import DeleteMsg
from config import Administrators

# -- code --


class TakeBackMsgCore(EventHandler, IMessageFilter):
    interested = [GroupMessage]

    entrys = [r"^\[CQ:reply,id=(?P<id>-?\d+)\](?:\[CQ:at,qq=\d+\])*\s*撤回$"]

    def run(self):
        super().run()
        p = rf"^\[CQ:reply,id=(?P<id>-?\d+)\](?:\[CQ:at,qq={self.bot.qq_number}\]\s*)*撤回$"
        self.entrys = [compile(p)]

    async def handle(self, evt: GroupMessage):
        if not evt.user_id in Administrators:
            return
        if not (r := self.filter(evt)):
            return
        id = r.get("id", "")

        await DeleteMsg(int(id)).do(self.bot)


@register_to("ALL")
class TakeBackMsg(Service):
    cores = [TakeBackMsgCore]
