# -- stdlib --
from re import RegexFlag

# -- third party --
# -- own --
from services.base import register_service_to, Service, IMessageFilter, EventHandler
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.wrapper import timecooling

# -- code --


class BakaResponseCore(EventHandler, IMessageFilter):
    interested = [GroupMessage]
    entrys = [
        r"^(你是|就是)?(?P<word>baka|バカ|大笨蛋|笨蛋)(!|！)*?$",
        r"^(?P<word2>(?:笨蛋|baka|バカ|蠢)+)(?:!|！)*?$",
    ]
    entry_flags = RegexFlag.I

    async def handle(self, evt: GroupMessage):
        if (r := self.filter(evt)) is not None:
            await self.response(r, evt.group_id)

    @timecooling(3)
    async def response(self, r, group_id):
        bot = self.bot
        if word := r.get("word", None):
            await SendGroupMsg(group_id=group_id, message="不是%s!" % word).do()
        elif r.get("word2", None):
            await SendGroupMsg(group_id=group_id, message="我不笨!").do()


@register_service_to("ALL")
class BakaResponse(Service):
    cores = [BakaResponseCore]
