# -- stdlib --
# -- third party --
import random

# -- own --
from services.base import register_service_to, Service, EventHandler, IMessageFilter
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg

# -- code --


class RollCore(EventHandler, IMessageFilter):
    interested = [GroupMessage]
    entrys = [r"^\.r\s*(?P<args>\d{,4}(?:d\d{,4})?(?:\s*\+\s*\d{,4}(?:d\d{,4})?)*)\s*$"]

    async def handle(self, evt: GroupMessage):
        if not (r := self.filter(evt)):
            return
        args = r.get("args", "").split("+")
        args = map(lambda x: x.strip(), args)

        result = 0
        exps = []
        for arg in args:
            if arg.isdigit():
                result += int(arg)
                exps.append(arg)
            else:
                c, l = arg.split("d")
                c = c or 1
                l = l or 100
                c, l = int(c), int(l)
                result += sum(random.randint(1, l) for _ in range(c))
                exps.append(f"{c}d{l}")
        m = f"[{evt.sender.card or evt.sender.nickname}]掷骰:{'+'.join(exps)}={result}"

        await SendGroupMsg(evt.group_id, m).do()


@register_service_to("ALL")
class Roll(Service):
    cores = [RollCore]
