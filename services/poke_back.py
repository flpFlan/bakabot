# -- stdlib --
# -- third party --
# -- own --
from services.base import register_to, Service, EventHandler
from cqhttp.events.notice import GroupPoked
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.wrapper import timecooling

# -- code --


class PokeBackCore(EventHandler):
    interested = [GroupPoked]

    async def handle(self, evt: GroupPoked):
        if not evt.target_id == self.bot.qq_number:
            return
        await self.pokeback(evt)

    @timecooling(2)
    async def pokeback(self, evt: GroupPoked):
        m = f"[CQ:poke,qq={evt.user_id}]"

        await SendGroupMsg(evt.group_id, m).do(self.bot)


@register_to("ALL")
class PokeBack(Service):
    cores = [PokeBackCore]
