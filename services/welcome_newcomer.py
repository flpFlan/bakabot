# -- stdlib --
import os

# -- third party --
# -- own --
from services.base import register_to, Service, EventHandler
from cqhttp.events.notice import GroupMemberIncreased
from cqhttp.api.message.SendGroupMsg import SendGroupMsg

# -- code --


class WelcomeNewcomerCore(EventHandler):
    interested = [GroupMemberIncreased]

    async def handle(self, evt: GroupMemberIncreased):
        if evt.user_id == self.bot.qq_number:
            return
        path = os.path.abspath("src/BAKA.gif")
        m = f"[CQ:at,qq={evt.user_id}]\n欢迎新人![CQ:image,file=file:///{path}]"

        await SendGroupMsg(evt.group_id, m).do(self.bot)


@register_to("ALL")
class WelcomeNewcomer(Service):
    cores = [WelcomeNewcomerCore]
