# -- stdlib --
# -- third party --
# -- own --
from services.base import Service.register, Service, EventHandler
from cqhttp.events.notice import GroupPoked
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.wrapper import cool_down_for
from cqhttp.cqcode import At

# -- code --


class PokeBackCore(EventHandler):
    interested = [GroupPoked]

    async def handle(self, evt: GroupPoked):
        if not evt.target_id == self.bot.qq_number:
            return
        await self.pokeback(evt)

    @cool_down_for(2)
    async def pokeback(self, evt: GroupPoked):
        m = f"{At(evt.user_id)}"

        await SendGroupMsg(evt.group_id, m).do()


@Service.register("ALL")
class PokeBack(Service):
    cores = [PokeBackCore]
