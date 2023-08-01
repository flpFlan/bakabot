# -- stdlib --
import os

# -- third party --
# -- own --
from services.base import Service, ServiceBehavior, OnEvent
from cqhttp.events.notice import GroupMemberIncreased
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from services.core.whitelist import whitelist
from cqhttp.cqcode import At, Image
from accio import ACCIO

# -- code --


class WelcomeNewcomer(Service):
    pass


class WelcomeNewcomerCore(ServiceBehavior[WelcomeNewcomer]):
    @OnEvent[GroupMemberIncreased].add_listener
    async def handle(self, evt: GroupMemberIncreased):
        if evt.user_id == ACCIO.bot.qq_number:
            return
        if evt.group_id not in whitelist:
            return
        path = os.path.abspath("src/BAKA.gif")
        m = f"{At(evt.user_id)}\n欢迎新人!{Image(f'file:///{path}')}"

        await SendGroupMsg(evt.group_id, m).do()
