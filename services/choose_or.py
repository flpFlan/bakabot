# -- stdlib --
import os
import random

# -- third party --
# -- own --
from services.base import register_to, Service, EventHandler, IMessageFilter
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg

# -- code --


class ChooseOrCore(EventHandler, IMessageFilter):
    interested = [GroupMessage]
    entrys = [r"^选择(?P<choices>.+还是.+)"]

    async def handle(self, evt: GroupMessage):
        if not (r := self.filter(evt)):
            return
        choices = r.get("choices", "").split("还是")
        if not all(choices):
            return
        final_choice = random.choice(choices)
        m = f"[CQ:at,qq={evt.user_id}]\n"
        for i, c in enumerate(choices):
            m += f"{i + 1}、{c}\n"
        m += f"建议你选择：{final_choice}"

        await SendGroupMsg(evt.group_id, m).do(self.bot)


@register_to("ALL")
class ChooseOr(Service):
    cores = [ChooseOrCore]
