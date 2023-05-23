# -- stdlib --
import os

# -- third party --
# -- own --
from services.base import register_service_to, Service, EventHandler
from cqhttp.events.notice import GroupMemberIncreased
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from services.core.whitelist import whitelist
from cqhttp.cqcode import At, Image

# -- code --


class WelcomeNewcomerCore(EventHandler):
    interested = [GroupMemberIncreased]

    async def handle(self, evt: GroupMemberIncreased):
        if evt.user_id == self.bot.qq_number:
            return
        if evt.group_id not in whitelist:
            return
        path = os.path.abspath("src/BAKA.gif")
        m = f"{At(evt.user_id)}\n欢迎新人!{Image(f'file:///{path}')}"

        await SendGroupMsg(evt.group_id, m).do()


@register_service_to("ALL")
class WelcomeNewcomer(Service):
    cores = [WelcomeNewcomerCore]
