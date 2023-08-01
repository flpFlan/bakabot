# -- stdlib --
# -- third party --
# -- own --
from services.base import Service, ServiceBehavior, OnEvent
from cqhttp.events.notice import GroupPoked
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.wrapper import cool_down_for
from cqhttp.cqcode import Poke
from accio import ACCIO

# -- code --


class PokeBack(Service):
    pass


class PokeBackCore(ServiceBehavior[PokeBack]):
    @OnEvent[GroupPoked].add_listener
    async def handle(self, evt: GroupPoked):
        if not evt.target_id == ACCIO.bot.qq_number:
            return
        await self.pokeback(evt)

    @cool_down_for(2)
    async def pokeback(self, evt: GroupPoked):
        m = f"{Poke(evt.user_id)}"

        await SendGroupMsg(evt.group_id, m).do()
