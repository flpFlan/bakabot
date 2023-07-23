# -- stdlib --
from re import RegexFlag

# -- own --
from services.base import IMessageFilter, Service, ServiceBehavior, OnEvent
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.wrapper import cool_down_for

# -- code --


class BakaResponse(Service):
    pass


class BakaResponseCore(ServiceBehavior[BakaResponse], IMessageFilter):
    entrys = [
        r"^(你是|就是)?(?P<word>baka|バカ|大笨蛋|笨蛋)(!|！)*?$",
        r"^(?P<word2>(?:笨蛋|baka|バカ|蠢)+)(?:!|！)*?$",
    ]
    entry_flags = RegexFlag.I

    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if r := self.filter(evt):
            await self.response(r.groupdict(), evt.group_id)

    @cool_down_for(seconds=3)
    async def response(self, r, group_id):
        if word := r.get("word"):
            await SendGroupMsg(group_id=group_id, message="不是%s!" % word).do()
        elif _ := r.get("word2"):
            await SendGroupMsg(group_id=group_id, message="我不笨!").do()
