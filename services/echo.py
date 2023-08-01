# -- stdlib --
from collections import defaultdict
import random

# -- third party --

# -- own --
from services.base import Service, ServiceBehavior, OnEvent
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from .game.base import ManagerCore

# -- code --


class Echo(Service):
    async def __setup(self):
        self.msg_graph: dict[int, list[str | None]] = defaultdict(lambda: [None, None])


class EchoCore(ServiceBehavior[Echo]):
    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if evt.group_id in ManagerCore.games:
            if ManagerCore.games[evt.group_id].get(evt.user_id):
                return
        cache = self.service.msg_graph[evt.group_id]
        m1, m2 = cache
        if m1 == m2 == evt.message:
            cache[0], cache[1] = None, None
            m = "你群天天复读" if evt.message != "你群天天复读" else self.get_echo()
            await SendGroupMsg(evt.group_id, m).do()
        else:
            cache[1] = m1
            cache[0] = evt.message

    def get_echo(self):
        e = ["天天", "你", "群", "读复"]
        random.shuffle(e)
        return "".join(e)
