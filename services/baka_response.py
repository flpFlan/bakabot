# -- stdlib --
from re import RegexFlag

# -- third party --
# -- own --
from services.base import register_to, Service, MessageHandler
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg

# -- code --


class BakaResponseCore(MessageHandler):
    interested = [GroupMessage]
    entrys = [
        r"^(你是|就是)?(?P<word>baka|バカ|大笨蛋|笨蛋)(!|！)*?$",
        r"^(?P<word2>笨蛋|baka|バカ|蠢)+(!|！)*?$",
    ]
    entry_flags = RegexFlag.I

    async def handle(self, evt: GroupMessage):
        if (r := self.fliter(evt)) is not None:
            bot = self.bot
            group_id = evt.group_id
            if word := r.get("word", None):
                await SendGroupMsg(group_id=group_id, message="不是%s!" % word).do(bot)
            elif word := r.get("word2", None):
                await SendGroupMsg(group_id=group_id, message="我不笨!" % word).do(bot)


@register_to("ALL")
class BakaResponse(Service):
    cores = [BakaResponseCore]
