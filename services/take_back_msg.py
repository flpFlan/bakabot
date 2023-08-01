# -- stdlib --
from re import compile

# -- third party --
# -- own --
from services.base import Service, ServiceBehavior, IMessageFilter, OnEvent
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.DeleteMsg import DeleteMsg
from accio import ACCIO

# -- code --


class TakeBackMsg(Service):
    pass


class TakeBackMsgCore(ServiceBehavior[TakeBackMsg], IMessageFilter):
    entrys = [r"^\[CQ:reply,id=(?P<id>-?\d+)\](?:\[CQ:at,qq=\d+\])*\s*撤回$"]

    async def __setup(self):
        p = rf"^\[CQ:reply,id=(?P<id>-?\d+)\](?:\[CQ:at,qq={ACCIO.bot.qq_number}\]\s*)*撤回$"
        self.entrys = [compile(p)]

    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if not evt.user_id in ACCIO.bot.Administrators:
            return
        if not (r := self.filter(evt)):
            return
        id = r["id"]

        await DeleteMsg(int(id)).do()
