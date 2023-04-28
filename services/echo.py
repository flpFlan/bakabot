# -- stdlib --
from collections import defaultdict
import random

# -- third party --

# -- own --
from typing import cast
from services.base import register_to, Service, EventHandler
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg

# -- code --


class EchoCore(EventHandler):
    interested = [GroupMessage]

    async def handle(self, evt: GroupMessage):
        cache = cast(Echo, self.service).msg_graph[evt.group_id]
        m1, m2 = cache
        if m1 == m2 == evt.message:
            cache[0], cache[1] = None, None
            m = "你群天天复读" if evt.message != "你群天天复读" else self.get_echo()
            await SendGroupMsg(evt.group_id, m).do(self.bot)
        else:
            cache[1] = m1
            cache[0] = evt.message

    def get_echo(self):
        e = ["天天", "你群", "读复"]
        random.shuffle(e)
        return "".join(e)


@register_to("ALL")
class Echo(Service):
    cores = [EchoCore]

    async def start(self):
        await super().start()
        self.msg_graph: dict[int, list[str | None]] = defaultdict(lambda: [None, None])
