# -- third party --
import random

# -- own --
from services.base import Service, ServiceBehavior, IMessageFilter, OnEvent
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg

# -- code --

doc = """
格式:
    .r <arg> [+ <arg> ...]
参数:
    <arg>: 骰子或常数
    骰子: <count>d<limit>
    常数: <number>
用例:
    .r1d100+1d20+1d10+10
""".strip()


class Roll(Service):
    name = "Roll点"
    doc = doc


class RollCore(ServiceBehavior[Roll], IMessageFilter):
    entrys = [r"^\.r\s*(?P<args>\d{,4}(?:d\d{,4})?(?:\s*\+\s*\d{,4}(?:d\d{,4})?)*)\s*$"]

    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if not (r := self.filter(evt)):
            return
        args = r.group("args").split("+")
        args = map(lambda x: x.strip(), args)

        result = 0
        exps = []
        for arg in args:
            if arg.isdigit():
                result += int(arg)
                exps.append(arg)
            else:
                c, l = (arg or "d").split("d")
                c = c or 1
                l = l or 100
                c, l = int(c), int(l)
                result += sum(random.randint(1, l) for _ in range(c))
                exps.append(f"{c}d{l}")
        m = f"[{evt.sender.card or evt.sender.nickname}]掷骰:{'+'.join(exps)}={result}"

        await SendGroupMsg(evt.group_id, m).do()
